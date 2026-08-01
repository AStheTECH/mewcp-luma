**Run your events end to end — create, ticket, discount, invite, and manage every guest.**

A Model Context Protocol (MCP) server that exposes Luma's API for event creation, ticketing, coupons, and guest management.


## Overview

The mewcp-luma MCP Server provides full lifecycle control over Luma events and their guests:

- Create and update events, ticket types, and discount coupons
- Add, invite, approve, decline, waitlist, and re-ticket guests
- Read event details, guest lists, ticket types, coupons, and calendar metadata

Perfect for:

- Automating event setup — event, tickets, pricing, and promo codes in one flow
- Running guest operations at scale — bulk adds, invites, and approval sweeps
- Reporting on registrations, check-ins, and ticket orders from an agent


## Tools


<details>
<summary><code>get_calendar</code> — Read the calendar's metadata</summary>

Retrieves details for a calendar and returns its metadata, including name, slug, URL, description, location, coordinates, and social handles.

**Inputs:**
```
(no parameters)
```

**Output `data` schema:**

```typescript
{
  id: string;
  name: string | null;
  slug: string | null;
  avatar_url: string | null;
  url: string | null;
  description: string | null;
  social_image_url: string | null;
  cover_image_url: string | null;
  is_personal: boolean | null;
  location: {
    city: string | null;
    region: string | null;
    country: string | null;
    country_code: string | null;
    timezone: string | null;
  } | null;
  coordinate: {
    longitude: number | null;
    latitude: number | null;
  } | null;
  instagram_handle: string | null;
  twitter_handle: string | null;
  youtube_handle: string | null;
  website: string | null;
}
```

</details>


<details>
<summary><code>get_event</code> — Read one event's full details</summary>

Retrieves the full details of a single event you have manage access for, including hosts and a breakdown of guest counts by status.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
```

**Output `data` schema:**

```typescript
{
  platform: string | null;
  id: string;
  user_id: string | null;
  calendar_id: string | null;
  start_at: string | null;
  duration_interval: string | null;
  end_at: string | null;
  created_at: string | null;
  timezone: string | null;
  name: string | null;
  geo_address_json: {
    address: string | null;
    city: string | null;
    region: string | null;
    country: string | null;
    city_state: string | null;
    full_address: string | null;
    google_maps_place_id: string | null;
    apple_maps_place_id: string | null;
    description: string | null;
  } | null;
  coordinate: {
    longitude: number | null;
    latitude: number | null;
  } | null;
  meeting_url: string | null;
  location_type: string | null;
  location_visibility: string | null;
  cover_url: string | null;
  registration_questions: {
    id: string | null;
    label: string | null;
    required: boolean | null;
    question_type: string | null;
    collect_job_title: boolean | null;
    job_title_label: string | null;
    options: string[] | null;
    terms: {
      content_type: string | null;
      content_md: string | null;
      collect_signature: boolean | null;
      require_review: boolean | null;
    } | null;
  }[] | null;
  url: string | null;
  visibility: string | null;
  waitlist_status: string | null;
  registration_open: boolean | null;
  require_approval: boolean | null;
  spots_remaining: number | null;
  display_price: {
    amount: number | null;
    currency: string | null;
    is_flexible: boolean | null;
  } | null;
  feedback_email: {
    enabled: boolean | null;
    delay: string | null;
  } | null;
  access: string | null;
  description: string | null;
  description_md: string | null;
  hosts: {
    id: string | null;
    email: string | null;
    name: string | null;
    first_name: string | null;
    last_name: string | null;
    avatar_url: string | null;
  }[] | null;
  guest_counts: {
    approved: { guests: number | null; tickets: number | null } | null;
    pending_approval: { guests: number | null; tickets: number | null } | null;
    waitlist: { guests: number | null; tickets: number | null } | null;
    invited: { guests: number | null; tickets: number | null } | null;
    declined: { guests: number | null; tickets: number | null } | null;
    checked_in: { guests: number | null; tickets: number | null } | null;
  } | null;
}
```

</details>


<details>
<summary><code>get_guest</code> — Read one guest, with ticket orders</summary>

Retrieves the details of a single guest for an event, including ticket order details.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `id` (string, required) — Guest identifier — the guest ID (gst-), a ticket key, a guest key (g-), or the user's email.
```

**Output `data` schema:**

```typescript
{
  id: string;
  user_id: string | null;
  user_email: string | null;
  user_name: string | null;
  user_first_name: string | null;
  user_last_name: string | null;
  approval_status: string | null;
  check_in_qr_code: string | null;
  eth_address: string | null;
  invited_at: string | null;
  joined_at: string | null;
  phone_number: string | null;
  registered_at: string | null;
  registration_answers: {
    label: string | null;
    question_id: string | null;
    value: any | null;
    question_type: string | null;
  }[] | null;
  solana_address: string | null;
  utm_source: string | null;
  event_tickets: {
    id: string | null;
    amount: number | null;
    amount_discount: number | null;
    amount_tax: number | null;
    currency: string | null;
    checked_in_at: string | null;
    event_ticket_type_id: string | null;
    is_captured: boolean | null;
    name: string | null;
  }[] | null;
  event_ticket_orders: {
    id: string | null;
    amount: number | null;
    amount_discount: number | null;
    amount_tax: number | null;
    currency: string | null;
    coupon_info: {
      api_id: string | null;
      percent_off: number | null;
      cents_off: number | null;
      currency: string | null;
      code: string | null;
    } | null;
    is_captured: boolean | null;
  }[] | null;
}
```

</details>


<details>
<summary><code>get_ticket_type</code> — Read one ticket type</summary>

Retrieves the details of a single ticket type.

**Inputs:**
```
- `event_ticket_type_id` (string, required) — Ticket type ID, this usually starts with ttype-.
```

**Output `data` schema:**

```typescript
{
  id: string;
  name: string | null;
  require_approval: boolean | null;
  is_hidden: boolean | null;
  description: string | null;
  valid_start_at: string | null;
  valid_end_at: string | null;
  max_capacity: number | null;
  type: string | null;
  cents: number | null;
  currency: string | null;
  is_flexible: boolean | null;
  min_cents: number | null;
}
```

</details>


<details>
<summary><code>list_event_coupons</code> — Page through an event's coupons</summary>

Returns a paginated list of coupons associated with an event.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `pagination_cursor` (string, optional, default: null) — Value of next_cursor from a previous request.
- `pagination_limit` (number, optional, default: null) — The number of items to return. The server enforces a maximum.
```

**Output `data` schema:**

```typescript
{
  entries: {
    id: string;
    code: string | null;
    remaining_count: integer | null;
    valid_start_at: string | null;
    valid_end_at: string | null;
    percent_off: number | null;
    cents_off: number | null;
    currency: string | null;
    event_ticket_type_id: string | null;
  }[];
  has_more: boolean | null;
  next_cursor: string | null;
}
```

</details>


<details>
<summary><code>list_guests</code> — Page through an event's guests</summary>

Returns a paginated list of guests who have registered or been invited to an event, including guest summaries and event_tickets (use get_guest for order-level detail).

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `approval_status` (string, optional, default: null) — Filter by status: approved, session, pending_approval, invited, declined, or waitlist.
- `pagination_cursor` (string, optional, default: null) — Value of next_cursor from a previous request.
- `pagination_limit` (number, optional, default: null) — The number of items to return. The server enforces a maximum.
- `sort_column` (string, optional, default: null) — name, email, created_at, registered_at, or checked_in_at.
- `sort_direction` (string, optional, default: null) — asc, desc, asc nulls last, or desc nulls last.
```

**Output `data` schema:**

```typescript
{
  entries: {
    id: string;
    user_id: string | null;
    user_email: string | null;
    user_name: string | null;
    user_first_name: string | null;
    user_last_name: string | null;
    approval_status: string | null;
    check_in_qr_code: string | null;
    eth_address: string | null;
    invited_at: string | null;
    joined_at: string | null;
    phone_number: string | null;
    registered_at: string | null;
    registration_answers: {
      label: string | null;
      question_id: string | null;
      value: any | null;
      question_type: string | null;
    }[] | null;
    solana_address: string | null;
    utm_source: string | null;
    event_tickets: {
      id: string | null;
      amount: number | null;
      amount_discount: number | null;
      amount_tax: number | null;
      currency: string | null;
      checked_in_at: string | null;
      event_ticket_type_id: string | null;
      is_captured: boolean | null;
      name: string | null;
    }[] | null;
  }[];
  has_more: boolean | null;
  next_cursor: string | null;
}
```

</details>


<details>
<summary><code>list_ticket_types</code> — List every ticket type on an event</summary>

Returns the full list of ticket types for an event in one response (not paginated).

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `include_hidden` (string, optional, default: null) — Include hidden ticket types in the results.
```

**Output `data` schema:**

```typescript
{
  entries: {
    id: string;
    name: string | null;
    require_approval: boolean | null;
    is_hidden: boolean | null;
    description: string | null;
    valid_start_at: string | null;
    valid_end_at: string | null;
    max_capacity: number | null;
    type: string | null;
    cents: number | null;
    currency: string | null;
    is_flexible: boolean | null;
    min_cents: number | null;
  }[];
}
```

</details>


<details>
<summary><code>request_event_cancellation</code> — Step 1 of cancelling: token + impact preview</summary>

Requests a short-lived cancellation token and impact preview (guest count, whether paid) for an event — the first step of Luma's two-step cancellation flow.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
```

**Output `data` schema:**

```typescript
{
  cancellation_token: string;
  is_paid: boolean | null;
  guest_count: number | null;
}
```

</details>


<details>
<summary><code>create_event</code> — Create a new event</summary>

Creates a new event and returns its id.

**Inputs:**
```
- `name` (string, required) — Event name.
- `start_at` (string, required) — ISO 8601 datetime the event starts.
- `timezone` (string, required) — IANA timezone, e.g. America/New_York.
- `can_register_for_multiple_tickets` (boolean, optional, default: null) — Whether a single guest can register for multiple tickets.
- `cover_url` (string, optional, default: null) — Cover image URL; must be hosted on the Luma CDN (images.lumacdn.com), uploaded via /v1/images/create-upload-url first.
- `coordinate` (object, optional, default: null) — {longitude, latitude} for the event location.
- `description_md` (string, optional, default: null) — Markdown description, converted internally to Luma's rich text format; embedded images must be hosted on the Luma CDN.
- `end_at` (string, optional, default: null) — ISO 8601 datetime the event ends.
- `geo_address_json` (object, optional, default: null) — Either {type: "manual", address} for a free-text address, or {type: "google", place_id, description?} for a Google Maps Place ID.
- `location_visibility` (string, optional, default: null) — public (default) or guests-only — hides the precise location from unapproved guests.
- `max_capacity` (number, optional, default: null) — Maximum registrations before the event is marked sold out (or guests join the waitlist, if enabled).
- `meeting_url` (string, optional, default: null) — Virtual meeting URL for online events.
- `name_requirement` (string, optional, default: null) — full-name or first-last — whether to split the guest name field into first/last.
- `phone_number_requirement` (string, optional, default: null) — optional or required — whether guests must supply a phone number at registration; omit to not collect it.
- `registration_open` (boolean, optional, default: null) — Whether to accept registrations. Defaults to true.
- `registration_questions` (object[], optional, default: null) — Custom registration questions; each object is discriminated by question_type (agree-check, company, dropdown, github, instagram, linkedin, long-text, multi-select, phone-number, telegram, text, twitter, url, youtube, terms).
- `reminders_disabled` (boolean, optional, default: null) — Turns off Luma's default pre-event reminder emails.
- `feedback_email` (object, optional, default: null) — {enabled, delay} settings for the post-event feedback email; delay defaults to PT0M, maximum P7D.
- `show_guest_list` (boolean, optional, default: null) — Whether approved guests can see who else is attending.
- `slug` (string, optional, default: null) — URL slug for the event page (luma.com/<slug>); creation fails if unavailable.
- `tint_color` (string, optional, default: null) — Hex color, e.g. #bb2dc7; alpha channels are stripped.
- `visibility` (string, optional, default: null) — public, members-only, or private.
- `waitlist_status` (string, optional, default: null) — disabled or enabled — whether new registrations join a waitlist once capacity is reached.
```

**Output `data` schema:**

```typescript
{
  id: string;
}
```

</details>


<details>
<summary><code>create_ticket_type</code> — Add a ticket type to an event</summary>

Creates a new ticket type for an event and returns the created ticket type, including its id.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `name` (string, required) — Ticket type name.
- `type` (string, required) — free or paid.
- `require_approval` (boolean, optional, default: null) — Whether registrations for this ticket type require host approval.
- `is_hidden` (boolean, optional, default: null) — Hides the ticket type from public view, e.g. for an invite-only tier.
- `description` (string, optional, default: null) — Ticket type description.
- `valid_start_at` (string, optional, default: null) — ISO 8601 date the ticket type becomes available.
- `valid_end_at` (string, optional, default: null) — ISO 8601 date the ticket type stops being available.
- `max_capacity` (number, optional, default: null) — Maximum number of this ticket type that can be issued.
- `cents` (number, optional, default: null) — Ticket price as an integer in the smallest unit of currency (e.g. cents for USD); only meaningful when type is paid.
- `currency` (string, optional, default: null) — Currency code for cents.
- `is_flexible` (boolean, optional, default: null) — Enables "pay what you want" pricing for a paid ticket.
- `min_cents` (number, optional, default: null) — Minimum amount a guest may pay when is_flexible is true.
```

**Output `data` schema:**

```typescript
{
  id: string;
  name: string | null;
  require_approval: boolean | null;
  is_hidden: boolean | null;
  description: string | null;
  valid_start_at: string | null;
  valid_end_at: string | null;
  max_capacity: number | null;
  type: string | null;
  cents: number | null;
  currency: string | null;
  is_flexible: boolean | null;
  min_cents: number | null;
}
```

</details>


<details>
<summary><code>create_coupon</code> — Create a discount or unlock code</summary>

Creates a new discount coupon for an event and returns the created coupon.

**Inputs:**
```
- `code` (string, required) — Code the guest enters on the event page. Case-insensitive, maximum 20 characters.
- `discount` (object, required) — Discriminated union: {discount_type: "percent", percent_off} (0-100), or {discount_type: "amount", cents_off, currency}.
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `remaining_count` (integer, optional, default: null) — Number of times the coupon can be used. Set to 1000000 for unlimited uses.
- `valid_start_at` (string, optional, default: null) — ISO 8601 datetime the coupon becomes valid.
- `valid_end_at` (string, optional, default: null) — ISO 8601 datetime the coupon expires.
- `event_ticket_type_id` (string, optional, default: null) — Restrict the coupon to a single ticket type. If that ticket type is hidden, the coupon acts as an unlock/access code instead of a discount.
```

**Output `data` schema:**

```typescript
{
  id: string;
  code: string | null;
  remaining_count: integer | null;
  valid_start_at: string | null;
  valid_end_at: string | null;
  percent_off: number | null;
  cents_off: number | null;
  currency: string | null;
  event_ticket_type_id: string | null;
}
```

</details>


<details>
<summary><code>add_guests</code> — Add guests straight onto an event</summary>

Adds one or more guests directly to an event (default status "Going", one ticket of the default type unless overridden) and returns an empty response on success.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `guests` (object[], required) — Guests to add, each requiring at least email; existing names are not overwritten. Each guest may include registration_answers (question_id + value) for the event's registration questions.
- `ticket` (object, optional, default: null) — Assign a single ticket of the specified event_ticket_type_id to each guest. Cannot be combined with tickets.
- `tickets` (object[], optional, default: null) — Assign multiple tickets (each by event_ticket_type_id) to each guest. Cannot be combined with ticket.
- `approval_status` (string, optional, default: null) — Status to assign each added guest: approved, pending_approval, or waitlist. Defaults to approved.
- `send_email` (boolean, optional, default: null) — Whether Luma should email each added guest. Defaults to true.
```

**Output `data` schema:**

```typescript
{
  event_id: string | null;
  guests_requested: integer | null;
}
```

</details>


<details>
<summary><code>send_invites</code> — Email soft invites to guests (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Sends one or more guests a soft invite to an event by email (and SMS if their phone is linked to their Luma account) that they can accept, returning an empty response on success. This sends real communications to every listed guest — the original invite state is not returned and cannot be recovered from this call. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly which guests will be invited and what the message will say, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `guests` (object[], required) — Guests to invite, each requiring at least email; existing names are not overwritten.
- `message` (string, optional, default: null) — Personalized message included in the invite. Maximum 200 characters.
```

**Output `data` schema:**

```typescript
{
  event_id: string | null;
  guests_invited: integer | null;
}
```

</details>


<details>
<summary><code>cancel_event</code> — Permanently cancel an event (destructive)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Cancels an event using a cancellation token from request_event_cancellation and returns an empty response on success. This action is irreversible — the event is deleted, all guests are notified, and refunds are processed if requested; the event cannot be recovered after this call. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what event will be permanently cancelled and that it is irreversible, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `cancellation_token` (string, required) — The cancellation token returned by request_event_cancellation.
- `should_refund` (boolean, optional, default: null) — Whether to refund paid guests. Conditionally required — must be set if the event has paid guests (see is_paid from request_event_cancellation).
```

**Output `data` schema:**

```typescript
{
  event_id: string | null;
}
```

</details>


<details>
<summary><code>update_event</code> — Update an event, with before/after state</summary>

Updates an existing event's details. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values, and the original values are not preserved after the call — the response includes both the before and after state (fetched via the same lookup as get_event) so you have a full record of what changed.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `suppress_notifications` (boolean, optional, default: null) — If true, guests are not notified (email/push) when the name, time, or location changes.
- `can_register_for_multiple_tickets` (boolean, optional, default: null) — Whether a single guest can register for multiple tickets.
- `cover_url` (string, optional, default: null) — Cover image URL; must be hosted on the Luma CDN (images.lumacdn.com).
- `coordinate` (object, optional, default: null) — {longitude, latitude} for the event location.
- `description_md` (string, optional, default: null) — Markdown description, converted internally to Luma's rich text format.
- `end_at` (string, optional, default: null) — ISO 8601 datetime the event ends.
- `geo_address_json` (object, optional, default: null) — Either {type: "manual", address} or {type: "google", place_id, description?}.
- `location_visibility` (string, optional, default: null) — public (default) or guests-only.
- `max_capacity` (number, optional, default: null) — Maximum registrations before the event is marked sold out (or joins the waitlist, if enabled).
- `meeting_url` (string, optional, default: null) — Virtual meeting URL for online events.
- `name` (string, optional, default: null) — Event name.
- `name_requirement` (string, optional, default: null) — full-name or first-last.
- `phone_number_requirement` (string, optional, default: null) — optional or required; omit to not collect it.
- `registration_open` (boolean, optional, default: null) — Whether to accept registrations.
- `registration_questions` (object[], optional, default: null) — Custom registration questions; each object is discriminated by question_type.
- `reminders_disabled` (boolean, optional, default: null) — Turns off Luma's default pre-event reminder emails.
- `feedback_email` (object, optional, default: null) — {enabled, delay} settings for the post-event feedback email.
- `show_guest_list` (boolean, optional, default: null) — Whether approved guests can see who else is attending.
- `slug` (string, optional, default: null) — URL slug for the event page; update fails if unavailable.
- `start_at` (string, optional, default: null) — ISO 8601 datetime the event starts.
- `timezone` (string, optional, default: null) — IANA timezone, e.g. America/New_York.
- `tint_color` (string, optional, default: null) — Hex color; alpha channels are stripped.
- `visibility` (string, optional, default: null) — public, members-only, or private.
- `waitlist_status` (string, optional, default: null) — disabled or enabled.
```

**Output `data` schema:**

`before` and `after` each carry the same shape as `get_event`'s `data`.

```typescript
{
  before: Event;
  after: Event;
}
```

</details>


<details>
<summary><code>update_guest_status</code> — Approve, decline, or waitlist a guest</summary>

Updates a guest's status (approved, declined, pending_approval, or waitlist), optionally refunding them and/or emailing a personal message. NOTE: this overwrites the guest's current status, and the original status is not preserved after the call — the response includes both the before and after state (fetched via the same lookup as get_guest) so you have a full record of what changed.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `guest_id` (string, required) — Guest identifier — the guest ID (gst-), a ticket key, a guest key (g-), or the user's email.
- `status` (string, required) — approved, declined, pending_approval, or waitlist.
- `should_refund` (boolean, optional, default: null) — If moving a paid guest to declined, waitlist, or pending_approval, whether to refund their payment. Defaults to false.
- `send_email` (boolean, optional, default: null) — Whether Luma should email the guest about the status change. Defaults to true.
- `message` (string, optional, default: null) — Personal message included in the status-change email. Maximum 200 characters. Can't be combined with send_email: false.
```

**Output `data` schema:**

`before` and `after` each carry the same shape as `get_guest`'s `data`.

```typescript
{
  before: Guest;
  after: Guest;
}
```

</details>


<details>
<summary><code>update_guest_tickets</code> — Grant or invalidate a guest's tickets</summary>

Administratively adds complimentary tickets to or removes/invalidates tickets from an existing guest with no payment or refund processed. NOTE: this overwrites the guest's ticket set, and the original ticket set is not preserved after the call — the response includes both the before and after state (fetched via the same lookup as get_guest) so you have a full record of what changed.

**Inputs:**
```
- `event_id` (string, required) — Event ID, this usually starts with evt-.
- `guest_id` (string, required) — Guest identifier — the guest ID (gst-), a ticket key, a guest key (g-), or the user's email.
- `ticket_ids_to_remove` (string[], optional, default: null) — Existing ticket IDs to invalidate. Removing tickets does not issue a refund, and at least one valid ticket must remain on the guest. Default [].
- `tickets_to_add` (object[], optional, default: null) — Complimentary tickets to grant (each by event_ticket_type_id); each entry creates a new $0 administrative ticket even for a normally paid ticket type. Default [].
- `send_email` (boolean, optional, default: null) — Whether Luma may email the guest about the ticket change. Defaults to true and still respects notification preferences.
```

**Output `data` schema:**

`before` and `after` each carry the same shape as `get_guest`'s `data`.

```typescript
{
  before: Guest;
  after: Guest;
}
```

</details>


<details>
<summary><code>update_ticket_type</code> — Update a ticket type, with before/after state</summary>

Updates an existing ticket type's details and returns the updated ticket type. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current field values — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `event_ticket_type_id` (string, required) — Ticket type ID, this usually starts with ttype-.
- `name` (string, optional, default: null) — Ticket type name.
- `require_approval` (boolean, optional, default: null) — Whether registrations for this ticket type require host approval.
- `is_hidden` (boolean, optional, default: null) — Hides the ticket type from public view.
- `description` (string, optional, default: null) — Ticket type description.
- `valid_start_at` (string, optional, default: null) — ISO 8601 date the ticket type becomes available.
- `valid_end_at` (string, optional, default: null) — ISO 8601 date the ticket type stops being available.
- `max_capacity` (number, optional, default: null) — Maximum number of this ticket type that can be issued.
- `type` (string, optional, default: null) — free or paid.
- `cents` (number, optional, default: null) — Ticket price as an integer in the smallest unit of currency; only meaningful when type is paid.
- `currency` (string, optional, default: null) — Currency code for cents.
- `is_flexible` (boolean, optional, default: null) — Enables "pay what you want" pricing for a paid ticket.
- `min_cents` (number, optional, default: null) — Minimum amount a guest may pay when is_flexible is true.
```

**Output `data` schema:**

`before` and `after` each carry the same shape as `get_ticket_type`'s `data`.

```typescript
{
  before: TicketType;
  after: TicketType;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "ticket and tickets cannot both be set", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `pagination_limit` — The number of items to return. The server enforces a maximum.
- `pagination_cursor` — Value of `next_cursor` from a previous request. Keep paging while `has_more` is `true`.
- `approval_status` — Guest status filter: `approved`, `session`, `pending_approval`, `invited`, `declined`, or `waitlist`.
- `sort_column` / `sort_direction` — Order guest results by `name`, `email`, `created_at`, `registered_at`, or `checked_in_at`, using `asc`, `desc`, `asc nulls last`, or `desc nulls last`.
- `send_email` — Whether Luma sends its own notification email for the action. Defaults to `true` where supported.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Event ID:**

```
evt-<identifier>
Example: evt-4KJDaiFgHYYYYYY
```

**Ticket type ID:**

```
ttype-<identifier>
Example: ttype-3nAdgWzEXXXXXX
```

**Guest identifier:**

```
gst-<identifier> | <ticket key> | g-<guest key> | <email address>
Example: gst-1YY0nkFZZZZZZZ
```

**Datetimes:**

```
ISO 8601
Example: 2026-08-14T18:00:00Z
```

</details>


## Getting Your Luma API Key

<details>
<summary><strong>Steps</strong></summary>

1. Go to [Luma](https://lu.ma) and open the calendar you want the key to act on
2. Open **Settings** for that calendar and select the **Options** tab
3. Find the **API** section and click **Create API Key** (an eligible Luma plan is required)
4. Copy the generated key — you will only see it once

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Luma credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Luma API key (static credential)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values — for example, `ticket` and `tickets` cannot both be set on `add_guests`, and `message` cannot be combined with `send_email: false` on `update_guest_status`

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `mewcp-luma/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Luma API Error</strong></summary>

- **Cause:** Upstream Luma API returned an error
- **Solution:**
  1. Check Luma service status at [Luma Status Page](https://status.lu.ma)
  2. Verify your credential has manage access to the event or calendar you are acting on
  3. Review the error message for specific details — expired `cancellation_token` values and unavailable `slug` values are common causes

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Luma API Documentation](https://docs.lu.ma/reference/getting-started-with-your-api)** — Official API reference
- **[Luma API Reference](https://docs.lu.ma/reference)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
