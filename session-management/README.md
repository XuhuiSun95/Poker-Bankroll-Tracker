## Session Management API (GraphQL) — Planning Doc

This doc outlines the planned GraphQL contract for session tracking. It aligns with the existing Strawberry GraphQL setup exposed at `POST /graphql`.

### Purpose and scope
- This service is the primary session management endpoint for a user's current session. It lets the authenticated user start, update, and end their current session.
- The API only exposes detailed information for the current session of the current user. It does not list historical sessions or support by-id lookups.
- Current session state is stored in Redis, keyed by `user_id`, with a TTL because a single session typically lasts no longer than a few days.
- All session transactions (e.g., rebuys, stack updates, hand notes, lifecycle events) are also published to Kafka for downstream ETL and long-term aggregation. Durable historical reporting should be built from Kafka, not from this service's Redis state.

### Base
- **Endpoint**: `POST /graphql`
- **Content-Type**: `application/json`
- **Auth**: The service associates sessions with the authenticated user via Keycloak OIDC. The `user_id` is derived from the access token (validated via JWKS). Clients do not provide any user identifiers in inputs.

### Environment variables
- `OIDC_AUTHORIZATION_URL` (required): OIDC authorization URL
- `OIDC_TOKEN_URL` (required): OIDC token URL
- `OIDC_JWKS_URL` (required): JWKS URL
- `OIDC_CLIENT_ID` (optional): Default `poker-bankroll-tracker`
- `OIDC_PERMITTED_AUDIENCES` (optional): Default `["account"]`
- `OIDC_APPLICATION_SCOPES_ENABLED` (optional, default `false`): when `true`, enforce `session:read` (queries/subscriptions) and `session:write` (mutations). DevOps must provision these scopes/roles in the IdP (e.g., Keycloak).

### Core Types
- **Session**: Represents a poker session (for the current user)
  - `status: SessionStatus!`
  - `version: Int!` (monotonically increasing; used for optimistic concurrency)
  - `playerName: String!`
  - `playerLocation: PlayerLocation!`
  - `gameType: GameType!`
  - `game: GameStakeType!` (union of `CashStake` or `TournamentStake`)
  - `buyIn: Money!`
  - `startTime: DateTime!`
  - `stopTime: DateTime`
  - `cashoutTime: DateTime`
  - `finalStack: Money`
  - `liveStack: Money`
  - `rebuys: [Rebuy!]!`
  - `stackUpdates: [StackUpdate!]!`
  - `handNotes: [HandNote!]!`
  - `createdAt: DateTime!`
  - `updatedAt: DateTime!`

- **GameStakeType** (union)
  - `CashStake`
    - `smallBlindCents: Int!`
    - `bigBlindCents: Int!`
    - `anteCents: Int` (0 or omitted if no ante)
  - `TournamentStake`
    - `smallBlindCents: Int`
    - `bigBlindCents: Int`
    - `anteCents: Int`

- **GameType**
  - Enum representing the session type
  - Allowed values:
    - `CASH_GAME`
    - `TOURNAMENT`

- **SessionStatus**
  - Enum representing lifecycle status
  - Allowed values: `ACTIVE`, `ENDED`

- **PlayerLocation**
  - Structured location info for the session
  - Fields (all optional):
    - `displayName: String` (e.g., "Bellagio, Las Vegas" or "Home Game")
    - `geo: GeoPoint` (latitude/longitude for visualization)
    - `address: String` (free-form postal address)
    - `placeId: String` (provider place identifier, e.g., Google Place ID)
    - `source: LocationSource` (where the location came from)

- **GeoPoint**
  - `latitude: Float!` (range -90..90)
  - `longitude: Float!` (range -180..180)

- **LocationSource**
  - Enum indicating provenance of the location
  - Allowed values: `USER_INPUT`, `GEOIP`, `PLACE_PICKER`, `OTHER`

- **Money**
  - `amountCents: Int!`
  - `currency: String!` (ISO 4217, e.g., "USD")

- **Rebuy**
  - `amount: Money!`
  - `at: DateTime!`

- **StackUpdate**
  - `stackAmount: Money!`
  - `at: DateTime!`

- **HandNote**
  - `at: DateTime!`
  - `text: String!`

- **SessionEvent**
  - Incremental update pushed over subscriptions
  - `version: Int!`
  - `status: SessionStatus`
  - `liveStack: Money`
  - `rebuys: [Rebuy!]`
  - `stackUpdates: [StackUpdate!]`
  - `handNotes: [HandNote!]`
  - `updatedAt: DateTime!`

Note: Monetary amounts are expressed in minor units (e.g., cents) to avoid floating point issues.

### Inputs
- `StartSessionInput`
  - `playerName: String!`
  - `playerLocation: PlayerLocationInput!`
  - `gameType: GameType!`
  - `game: GameStakeInput!`
  - `buyIn: MoneyInput!`
  - `startTime: DateTime!`

- `GameStakeInput`
  - `smallBlindCents: Int` (optional for `TOURNAMENT`; required for `CASH_GAME`)
  - `bigBlindCents: Int` (optional for `TOURNAMENT`; required for `CASH_GAME`)
  - `anteCents: Int` (optional; may be omitted for `TOURNAMENT`)

- `PlayerLocationInput`
  - `displayName: String`
  - `geo: GeoPointInput`
  - `address: String`
  - `placeId: String`
  - `source: LocationSource`

- `GeoPointInput`
  - `latitude: Float!`
  - `longitude: Float!`

- `MoneyInput`
  - `amountCents: Int!`
  - `currency: String!`

- `AppendSessionEventsInput`
  - `expectedVersion: Int` (optional optimistic concurrency check)
  - `rebuys: [RebuyInput!]` (optional, one or many)
  - `stackUpdates: [StackUpdateInput!]` (optional)
  - `handNotes: [HandNoteInput!]` (optional)

- `RebuyInput`
  - `amount: MoneyInput!`
  - `at: DateTime!`

- `StackUpdateInput`
  - `stackAmount: MoneyInput!`
  - `at: DateTime!`

- `HandNoteInput`
  - `at: DateTime!`
  - `text: String!`

- `EndSessionInput`
  - `expectedVersion: Int`
  - `stopTime: DateTime!`
  - `cashoutTime: DateTime!`
  - `finalStack: MoneyInput` (optional; if omitted, last stack update is used)

### Operations
- **Queries**
  - `currentSession: Session` (returns the current user's session)
  - `hasCurrentSession: Boolean!`

- **Mutations**
  - `startSession(input: StartSessionInput!): Session!`
  - `appendSessionEvents(input: AppendSessionEventsInput!): Session!`
  - `endSession(input: EndSessionInput!): Session!`
  - `discardSession: Boolean!`

- **Subscriptions**
  - `sessionEvents: SessionEvent!` (streams real-time events for the current user's session)

Implementation status
- Implemented: `currentSession`, `hasCurrentSession`, `startSession` (temporary simplified args)
- Planned: `appendSessionEvents`, `endSession`, `discardSession`, `sessionEvents`

### Examples

Start a session (current impl):

```graphql
mutation Start {
  startSession(
    playerName: "Alice"
    playerLocationDisplayName: "Bellagio, Las Vegas"
    gameType: CASH_GAME
  ) {
    status
    version
    playerName
    gameType
    buyIn { amountCents currency }
    createdAt
  }
}
```

Start a session (planned input signature):

```graphql
mutation Start {
  startSession(
    input: {
      playerName: "Alice"
      playerLocation: {
        displayName: "Bellagio, Las Vegas"
        geo: { latitude: 36.1125, longitude: -115.1767 }
      }
      gameType: CASH_GAME
      game: { smallBlindCents: 100, bigBlindCents: 200, anteCents: 0 }
      buyIn: { amountCents: 20000, currency: "USD" }
      startTime: "2025-08-09T16:30:00Z"
    }
  ) {
    status
    version
    playerName
    playerLocation { displayName geo { latitude longitude } }
    gameType
    game {
      ... on CashStake { smallBlindCents bigBlindCents anteCents }
      ... on TournamentStake { smallBlindCents bigBlindCents anteCents }
    }
    buyIn { amountCents currency }
    startTime
    createdAt
  }
}
```

Create a tournament session (all stake fields optional due to dynamic levels):

```graphql
mutation StartTournament {
  startSession(
    input: {
      playerName: "Bob"
      playerLocation: {
        displayName: "WSOP, Las Vegas"
        geo: { latitude: 36.1170, longitude: -115.1760 }
      }
      gameType: TOURNAMENT
      game: {}
      buyIn: { amountCents: 100000, currency: "USD" }
      startTime: "2025-08-10T12:00:00Z"
    }
  ) {
    status
    version
    playerName
    playerLocation { displayName geo { latitude longitude } }
    gameType
    game {
      ... on CashStake { smallBlindCents bigBlindCents anteCents }
      ... on TournamentStake { smallBlindCents bigBlindCents anteCents }
    }
    buyIn { amountCents currency }
    startTime
    createdAt
  }
}
```

Append session events (batched):

```graphql
mutation AppendEvents {
  appendSessionEvents(
    input: {
      expectedVersion: 3
      rebuys: [{ amount: { amountCents: 10000, currency: "USD" }, at: "2025-08-09T18:00:00Z" }]
      stackUpdates: [
        { stackAmount: { amountCents: 28000, currency: "USD" }, at: "2025-08-09T19:00:00Z" }
        { stackAmount: { amountCents: 24000, currency: "USD" }, at: "2025-08-09T20:00:00Z" }
      ]
      handNotes: [
        { at: "2025-08-09T19:05:00Z", text: "3-bet shove with AKs vs CO" }
      ]
    }
  ) {
    version
    liveStack { amountCents currency }
    rebuys { amount { amountCents currency } at }
    stackUpdates { stackAmount { amountCents currency } at }
    handNotes { at text }
    updatedAt
  }
}
```

End session:

```graphql
mutation End {
  endSession(
    input: {
      expectedVersion: 5
      stopTime: "2025-08-09T22:30:00Z"
      cashoutTime: "2025-08-09T22:40:00Z"
      finalStack: { amountCents: 31000, currency: "USD" }
    }
  ) {
    status
    stopTime
    cashoutTime
    finalStack { amountCents currency }
    updatedAt
  }
}
```

Fetch the current session:

```graphql
query GetOne {
  currentSession {
    status
    version
    playerName
    playerLocation {
      displayName
      geo { latitude longitude }
      address
      placeId
      source
    }
    gameType
    game {
      ... on CashStake { smallBlindCents bigBlindCents anteCents }
      ... on TournamentStake { smallBlindCents bigBlindCents anteCents }
    }
    buyIn { amountCents currency }
    startTime
    stopTime
    cashoutTime
    finalStack { amountCents currency }
    liveStack { amountCents currency }
    rebuys { amount { amountCents currency } at }
    stackUpdates { stackAmount { amountCents currency } at }
    handNotes { at text }
    createdAt
    updatedAt
  }
}
```

Check if a current session exists:

```graphql
query HasSession {
  hasCurrentSession
}
```

Discard the current session:

```graphql
mutation Discard {
  discardSession
}
```

### Notes
- Time values are ISO-8601 strings in UTC.
- Money values use integer minor units (e.g., cents) with a `currency` code.
- Internally, mid-session updates may be modeled as append-only events. This API supports batching to minimize round trips.
- Health endpoints already exist: `GET /liveness`, `GET /readiness`.
- Game type must be one of `CASH_GAME` or `TOURNAMENT`.
- For `TOURNAMENT` sessions, `smallBlindCents`, `bigBlindCents`, and `anteCents` in `GameStake`/`GameStakeInput` may be omitted because blind/ante levels change dynamically.
- Locations use WGS84 coordinates. If both `geo` and `address` are provided, `geo` is the source of truth for mapping.
- No explicit session `id` is used. The current session is keyed by `user_id` in the Redis state store and looked up via the authenticated context.

#### Invariants and validation
- Versioning: `version` increments by 1 per successful state-changing mutation (`startSession`, `appendSessionEvents`, `endSession`, `discardSession`).
- Currency consistency: All `MoneyInput` fields must use the same currency as `buyIn`.
- Timestamp ordering: `startTime` ≤ any `event.at` ≤ `cashoutTime` (if set) and `stopTime` ≤ `cashoutTime`.
- Game rules: `CASH_GAME` requires `smallBlindCents` and `bigBlindCents`; `TOURNAMENT` may omit all stake fields.
- Append validation: `appendSessionEvents` must include at least one of `rebuys`, `stackUpdates`, or `handNotes`.
- Live stack invariant: If `stackUpdates` is non-empty, the last `stackUpdates.stackAmount` equals `liveStack`.
- End semantics: `endSession` sets `liveStack = finalStack` (if provided) and appends a stack update at `cashoutTime`.

#### TTL and state lifecycle
- Redis TTL: The session key has a TTL (sessions are short-lived). The TTL is refreshed on state-changing mutations. Optionally, a server-side heartbeat may extend TTL while the session is ACTIVE.

#### Auth and roles
- All operations require authentication. Suggested scopes: `session:read` for queries/subscriptions; `session:write` for mutations.

#### Subscription delivery guarantees
- Ordering: Events are delivered in order for a given user. Delivery is at-least-once; clients de-duplicate using `version`.
- Startup snapshot: Upon subscribing to `sessionEvents`, the server first emits a snapshot of current state, then incremental updates.

### Subscriptions
`subscription sessionEvents` streams session updates (rebuys, stack updates, hand notes, lifecycle changes) for the current user in real time.

Transport/auth notes:
- Uses WebSocket protocol (e.g., `graphql-transport-ws`).
- Send the access token in the connection init; the server validates via Keycloak JWKS.
- The server scopes the stream to the authenticated `user_id`.

Example:
```graphql
subscription SessionEvents {
  sessionEvents {
    version
    status
    liveStack { amountCents currency }
    rebuys { amount { amountCents currency } at }
    stackUpdates { stackAmount { amountCents currency } at }
    handNotes { at text }
    updatedAt
  }
}
```

### Error handling
- `currentSession` returns `null` when no active session exists.
- Mutations use consistent error messages for validation and concurrency:
  - `CONFLICT` when `expectedVersion` does not match the current version.
  - `INVALID_INPUT` for schema/validation errors.
  - `NOT_ACTIVE` when attempting to mutate an ended or missing session.
