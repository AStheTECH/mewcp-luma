from typing import Any

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


# ---------------------------------------------------------------------------
# Shared nested models
# ---------------------------------------------------------------------------

class GeoAddressJson(BaseModel):
    model_config = ConfigDict(extra="allow")

    address: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    city_state: str | None = None
    full_address: str | None = None
    google_maps_place_id: str | None = None
    apple_maps_place_id: str | None = None
    description: str | None = None


class EventCoordinate(BaseModel):
    model_config = ConfigDict(extra="allow")

    longitude: float | None = None
    latitude: float | None = None


class RegistrationQuestionTerms(BaseModel):
    model_config = ConfigDict(extra="allow")

    content_type: str | None = None
    content_md: str | None = None
    collect_signature: bool | None = None
    require_review: bool | None = None


class RegistrationQuestion(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    label: str | None = None
    required: bool | None = None
    question_type: str | None = None
    collect_job_title: bool | None = None
    job_title_label: str | None = None
    options: list[str] | None = None
    terms: RegistrationQuestionTerms | None = None


class DisplayPrice(BaseModel):
    model_config = ConfigDict(extra="allow")

    amount: float | None = None
    currency: str | None = None
    is_flexible: bool | None = None


class FeedbackEmailInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool | None = None
    delay: str | None = None


class EventHost(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    email: str | None = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None


class GuestCountBucket(BaseModel):
    model_config = ConfigDict(extra="allow")

    guests: float | None = None
    tickets: float | None = None


class GuestCounts(BaseModel):
    model_config = ConfigDict(extra="allow")

    approved: GuestCountBucket | None = None
    pending_approval: GuestCountBucket | None = None
    waitlist: GuestCountBucket | None = None
    invited: GuestCountBucket | None = None
    declined: GuestCountBucket | None = None
    checked_in: GuestCountBucket | None = None


class RegistrationAnswer(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: str | None = None
    question_id: str | None = None
    value: Any | None = None
    question_type: str | None = None


class EventTicket(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    amount: float | None = None
    amount_discount: float | None = None
    amount_tax: float | None = None
    currency: str | None = None
    checked_in_at: str | None = None
    event_ticket_type_id: str | None = None
    is_captured: bool | None = None
    name: str | None = None


class CouponInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    api_id: str | None = None
    percent_off: float | None = None
    cents_off: float | None = None
    currency: str | None = None
    code: str | None = None


class EventTicketOrder(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    amount: float | None = None
    amount_discount: float | None = None
    amount_tax: float | None = None
    currency: str | None = None
    coupon_info: CouponInfo | None = None
    is_captured: bool | None = None


class GuestData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    user_id: str | None = None
    user_email: str | None = None
    user_name: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
    approval_status: str | None = None
    check_in_qr_code: str | None = None
    eth_address: str | None = None
    invited_at: str | None = None
    joined_at: str | None = None
    phone_number: str | None = None
    registered_at: str | None = None
    registration_answers: list[RegistrationAnswer] | None = None
    solana_address: str | None = None
    utm_source: str | None = None
    event_tickets: list[EventTicket] | None = None


class TicketTypeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    require_approval: bool | None = None
    is_hidden: bool | None = None
    description: str | None = None
    valid_start_at: str | None = None
    valid_end_at: str | None = None
    max_capacity: float | None = None
    type: str | None = None
    cents: float | None = None
    currency: str | None = None
    is_flexible: bool | None = None
    min_cents: float | None = None


class CouponData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    code: str | None = None
    remaining_count: int | None = None
    valid_start_at: str | None = None
    valid_end_at: str | None = None
    percent_off: float | None = None
    cents_off: float | None = None
    currency: str | None = None
    event_ticket_type_id: str | None = None


# ---------------------------------------------------------------------------
# add_guests
# ---------------------------------------------------------------------------

class GuestAddData(BaseModel):
    model_config = ConfigDict(extra="allow")

    event_id: str | None = None
    guests_requested: int | None = None


class GuestAddResult(ToolResult):
    data: GuestAddData | None = None


# ---------------------------------------------------------------------------
# cancel_event
# ---------------------------------------------------------------------------

class EventCancelData(BaseModel):
    model_config = ConfigDict(extra="allow")

    event_id: str | None = None


class EventCancelResult(ToolResult):
    data: EventCancelData | None = None


# ---------------------------------------------------------------------------
# create_coupon
# ---------------------------------------------------------------------------

class CouponCreateData(CouponData):
    pass


class CouponCreateResult(ToolResult):
    data: CouponCreateData | None = None


# ---------------------------------------------------------------------------
# create_event
# ---------------------------------------------------------------------------

class EventCreateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str


class EventCreateResult(ToolResult):
    data: EventCreateData | None = None


# ---------------------------------------------------------------------------
# create_ticket_type
# ---------------------------------------------------------------------------

class TicketTypeCreateData(TicketTypeData):
    pass


class TicketTypeCreateResult(ToolResult):
    data: TicketTypeCreateData | None = None


# ---------------------------------------------------------------------------
# get_event
# ---------------------------------------------------------------------------

class EventGetData(BaseModel):
    model_config = ConfigDict(extra="allow")

    platform: str | None = None
    id: str
    user_id: str | None = None
    calendar_id: str | None = None
    start_at: str | None = None
    duration_interval: str | None = None
    end_at: str | None = None
    created_at: str | None = None
    timezone: str | None = None
    name: str | None = None
    geo_address_json: GeoAddressJson | None = None
    coordinate: EventCoordinate | None = None
    meeting_url: str | None = None
    location_type: str | None = None
    location_visibility: str | None = None
    cover_url: str | None = None
    registration_questions: list[RegistrationQuestion] | None = None
    url: str | None = None
    visibility: str | None = None
    waitlist_status: str | None = None
    registration_open: bool | None = None
    require_approval: bool | None = None
    spots_remaining: float | None = None
    display_price: DisplayPrice | None = None
    feedback_email: FeedbackEmailInfo | None = None
    access: str | None = None
    description: str | None = None
    description_md: str | None = None
    hosts: list[EventHost] | None = None
    guest_counts: GuestCounts | None = None


class EventGetResult(ToolResult):
    data: EventGetData | None = None


# ---------------------------------------------------------------------------
# get_guest
# ---------------------------------------------------------------------------

class GuestGetData(GuestData):
    event_ticket_orders: list[EventTicketOrder] | None = None


class GuestGetResult(ToolResult):
    data: GuestGetData | None = None


# ---------------------------------------------------------------------------
# get_ticket_type
# ---------------------------------------------------------------------------

class TicketTypeGetData(TicketTypeData):
    pass


class TicketTypeGetResult(ToolResult):
    data: TicketTypeGetData | None = None


# ---------------------------------------------------------------------------
# list_event_coupons
# ---------------------------------------------------------------------------

class EventCouponListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    entries: list[CouponData]
    has_more: bool | None = None
    next_cursor: str | None = None


class EventCouponListResult(ToolResult):
    data: EventCouponListData | None = None


# ---------------------------------------------------------------------------
# list_guests
# ---------------------------------------------------------------------------

class GuestListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    entries: list[GuestData]
    has_more: bool | None = None
    next_cursor: str | None = None


class GuestListResult(ToolResult):
    data: GuestListData | None = None


# ---------------------------------------------------------------------------
# list_ticket_types
# ---------------------------------------------------------------------------

class TicketTypeListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    entries: list[TicketTypeData]


class TicketTypeListResult(ToolResult):
    data: TicketTypeListData | None = None


# ---------------------------------------------------------------------------
# request_event_cancellation
# ---------------------------------------------------------------------------

class EventCancellationRequestData(BaseModel):
    model_config = ConfigDict(extra="allow")

    cancellation_token: str
    is_paid: bool | None = None
    guest_count: float | None = None


class EventCancellationRequestResult(ToolResult):
    data: EventCancellationRequestData | None = None


# ---------------------------------------------------------------------------
# send_invites
# ---------------------------------------------------------------------------

class InviteSendData(BaseModel):
    model_config = ConfigDict(extra="allow")

    event_id: str | None = None
    guests_invited: int | None = None


class InviteSendResult(ToolResult):
    data: InviteSendData | None = None


# ---------------------------------------------------------------------------
# update_event
# ---------------------------------------------------------------------------
# The update API returns an empty body on success, so "before" and "after"
# are each captured via a discovery call to get_event's endpoint — once prior
# to updating, once after.

class EventUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: EventGetData
    after: EventGetData


class EventUpdateResult(ToolResult):
    data: EventUpdateData | None = None


# ---------------------------------------------------------------------------
# update_guest_status
# ---------------------------------------------------------------------------
# Same empty-body situation as update_event — "before"/"after" are captured
# via discovery calls to get_guest's endpoint.

class GuestStatusUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GuestGetData
    after: GuestGetData


class GuestStatusUpdateResult(ToolResult):
    data: GuestStatusUpdateData | None = None


# ---------------------------------------------------------------------------
# update_guest_tickets
# ---------------------------------------------------------------------------
# Same empty-body situation as update_event — "before"/"after" are captured
# via discovery calls to get_guest's endpoint (guest tickets are part of the
# guest resource).

class GuestTicketUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GuestGetData
    after: GuestGetData


class GuestTicketUpdateResult(ToolResult):
    data: GuestTicketUpdateData | None = None


# ---------------------------------------------------------------------------
# update_ticket_type
# ---------------------------------------------------------------------------
# The API does return the updated ticket type here, so this is the one UPDATE
# tool in this group with a genuine before/after pair (before is captured via
# a discovery call to get_ticket_type's endpoint prior to updating).

class TicketTypeUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: TicketTypeData
    after: TicketTypeData


class TicketTypeUpdateResult(ToolResult):
    data: TicketTypeUpdateData | None = None
