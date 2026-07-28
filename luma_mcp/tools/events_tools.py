"""Events group: add_guests, cancel_event, create_coupon, create_event, create_ticket_type,
get_event, get_guest, get_ticket_type, list_event_coupons, list_guests, list_ticket_types,
request_event_cancellation, send_invites, update_event, update_guest_status,
update_guest_tickets, update_ticket_type."""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.events import (
    CouponCreateData, CouponCreateResult,
    EventCancelData, EventCancelResult,
    EventCancellationRequestData, EventCancellationRequestResult,
    EventCouponListData, EventCouponListResult,
    EventCreateData, EventCreateResult,
    EventGetData, EventGetResult,
    EventUpdateData, EventUpdateResult,
    GuestAddData, GuestAddResult,
    GuestGetData, GuestGetResult,
    GuestListData, GuestListResult,
    GuestStatusUpdateData, GuestStatusUpdateResult,
    GuestTicketUpdateData, GuestTicketUpdateResult,
    InviteSendData, InviteSendResult,
    TicketTypeCreateData, TicketTypeCreateResult,
    TicketTypeData,
    TicketTypeGetData, TicketTypeGetResult,
    TicketTypeListData, TicketTypeListResult,
    TicketTypeUpdateData, TicketTypeUpdateResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("luma-mcp.tools.events")


def _body(**kwargs: Any) -> dict[str, Any]:
    """Build a request body, dropping unset (None) fields."""
    return {k: v for k, v in kwargs.items() if v is not None}


def register_events_tools(mcp: FastMCP) -> None:

    # ------------------------------------------------------------------
    # get_event
    # ------------------------------------------------------------------
    @mcp.tool(
        name="get_event",
        description=(
            "Retrieves the full details of a single event you have manage access for, "
            "including hosts and a breakdown of guest counts by status."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_event(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
    ) -> EventGetResult:
        tlog = ToolLogger(logger, "get_event")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/v1/events/get", params={"event_id": event_id},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return EventGetResult(success=True, statusCode=status, data=EventGetData(**data))
            return _upstream_err(EventGetResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EventGetResult, tlog, exc)

    # ------------------------------------------------------------------
    # get_guest
    # ------------------------------------------------------------------
    @mcp.tool(
        name="get_guest",
        description=(
            "Retrieves the details of a single guest for an event, including ticket order details."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_guest(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        id: str = Field(description="Guest identifier — the guest ID (gst-), a ticket key, a guest key (g-), or the user's email."),
    ) -> GuestGetResult:
        tlog = ToolLogger(logger, "get_guest")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/v1/events/guests/get", params={"event_id": event_id, "id": id},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return GuestGetResult(success=True, statusCode=status, data=GuestGetData(**data))
            return _upstream_err(GuestGetResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GuestGetResult, tlog, exc)

    # ------------------------------------------------------------------
    # get_ticket_type
    # ------------------------------------------------------------------
    @mcp.tool(
        name="get_ticket_type",
        description="Retrieves the details of a single ticket type.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_ticket_type(
        event_ticket_type_id: str = Field(description="Ticket type ID, this usually starts with ttype-."),
    ) -> TicketTypeGetResult:
        tlog = ToolLogger(logger, "get_ticket_type")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/v1/events/ticket-types/get",
                params={"event_ticket_type_id": event_ticket_type_id},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return TicketTypeGetResult(success=True, statusCode=status, data=TicketTypeGetData(**data))
            return _upstream_err(TicketTypeGetResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(TicketTypeGetResult, tlog, exc)

    # ------------------------------------------------------------------
    # list_event_coupons
    # ------------------------------------------------------------------
    @mcp.tool(
        name="list_event_coupons",
        description="Returns a paginated list of coupons associated with an event.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_event_coupons(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        pagination_cursor: str | None = Field(default=None, description="Value of next_cursor from a previous request."),
        pagination_limit: float | None = Field(default=None, description="The number of items to return. The server enforces a maximum."),
    ) -> EventCouponListResult:
        tlog = ToolLogger(logger, "list_event_coupons")

        try:
            params = _body(
                event_id=event_id,
                pagination_cursor=pagination_cursor,
                pagination_limit=pagination_limit,
            )
            data, status, retry_after = service.api_request(
                "GET", "/v1/events/coupons/list", params=params,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return EventCouponListResult(success=True, statusCode=status, data=EventCouponListData(**data))
            return _upstream_err(EventCouponListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EventCouponListResult, tlog, exc)

    # ------------------------------------------------------------------
    # list_guests
    # ------------------------------------------------------------------
    @mcp.tool(
        name="list_guests",
        description=(
            "Returns a paginated list of guests who have registered or been invited to an event, "
            "including guest summaries and event_tickets (use get_guest for order-level detail)."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_guests(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        approval_status: str | None = Field(default=None, description="Filter by status: approved, session, pending_approval, invited, declined, or waitlist."),
        pagination_cursor: str | None = Field(default=None, description="Value of next_cursor from a previous request."),
        pagination_limit: float | None = Field(default=None, description="The number of items to return. The server enforces a maximum."),
        sort_column: str | None = Field(default=None, description="name, email, created_at, registered_at, or checked_in_at."),
        sort_direction: str | None = Field(default=None, description="asc, desc, asc nulls last, or desc nulls last."),
    ) -> GuestListResult:
        tlog = ToolLogger(logger, "list_guests")

        try:
            params = _body(
                event_id=event_id,
                approval_status=approval_status,
                pagination_cursor=pagination_cursor,
                pagination_limit=pagination_limit,
                sort_column=sort_column,
                sort_direction=sort_direction,
            )
            data, status, retry_after = service.api_request(
                "GET", "/v1/events/guests/list", params=params,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return GuestListResult(success=True, statusCode=status, data=GuestListData(**data))
            return _upstream_err(GuestListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GuestListResult, tlog, exc)

    # ------------------------------------------------------------------
    # list_ticket_types
    # ------------------------------------------------------------------
    @mcp.tool(
        name="list_ticket_types",
        description="Returns the full list of ticket types for an event in one response (not paginated).",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_ticket_types(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        include_hidden: str | None = Field(default=None, description="Include hidden ticket types in the results."),
    ) -> TicketTypeListResult:
        tlog = ToolLogger(logger, "list_ticket_types")

        try:
            params = _body(event_id=event_id, include_hidden=include_hidden)
            data, status, retry_after = service.api_request(
                "GET", "/v1/events/ticket-types/list", params=params,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return TicketTypeListResult(success=True, statusCode=status, data=TicketTypeListData(**data))
            return _upstream_err(TicketTypeListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(TicketTypeListResult, tlog, exc)

    # ------------------------------------------------------------------
    # request_event_cancellation
    # ------------------------------------------------------------------
    @mcp.tool(
        name="request_event_cancellation",
        description=(
            "Requests a short-lived cancellation token and impact preview (guest count, whether "
            "paid) for an event — the first step of Luma's two-step cancellation flow."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def request_event_cancellation(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
    ) -> EventCancellationRequestResult:
        tlog = ToolLogger(logger, "request_event_cancellation")

        try:
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/cancel/request", body={"event_id": event_id},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return EventCancellationRequestResult(
                    success=True, statusCode=status, data=EventCancellationRequestData(**data),
                )
            return _upstream_err(EventCancellationRequestResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EventCancellationRequestResult, tlog, exc)

    # ------------------------------------------------------------------
    # create_event
    # ------------------------------------------------------------------
    @mcp.tool(
        name="create_event",
        description="Creates a new event and returns its id.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_event(
        name: str = Field(description="Event name."),
        start_at: str = Field(description="ISO 8601 datetime the event starts."),
        timezone: str = Field(description="IANA timezone, e.g. America/New_York."),
        can_register_for_multiple_tickets: bool | None = Field(default=None, description="Whether a single guest can register for multiple tickets."),
        cover_url: str | None = Field(default=None, description="Cover image URL; must be hosted on the Luma CDN (images.lumacdn.com), uploaded via /v1/images/create-upload-url first."),
        coordinate: dict[str, Any] | None = Field(default=None, description="{longitude, latitude} for the event location."),
        description_md: str | None = Field(default=None, description="Markdown description, converted internally to Luma's rich text format; embedded images must be hosted on the Luma CDN."),
        end_at: str | None = Field(default=None, description="ISO 8601 datetime the event ends."),
        geo_address_json: dict[str, Any] | None = Field(default=None, description="Either {type: \"manual\", address} for a free-text address, or {type: \"google\", place_id, description?} for a Google Maps Place ID."),
        location_visibility: str | None = Field(default=None, description="public (default) or guests-only — hides the precise location from unapproved guests."),
        max_capacity: float | None = Field(default=None, description="Maximum registrations before the event is marked sold out (or guests join the waitlist, if enabled)."),
        meeting_url: str | None = Field(default=None, description="Virtual meeting URL for online events."),
        name_requirement: str | None = Field(default=None, description="full-name or first-last — whether to split the guest name field into first/last."),
        phone_number_requirement: str | None = Field(default=None, description="optional or required — whether guests must supply a phone number at registration; omit to not collect it."),
        registration_open: bool | None = Field(default=None, description="Whether to accept registrations. Defaults to true."),
        registration_questions: list[dict[str, Any]] | None = Field(default=None, description="Custom registration questions; each object is discriminated by question_type (agree-check, company, dropdown, github, instagram, linkedin, long-text, multi-select, phone-number, telegram, text, twitter, url, youtube, terms)."),
        reminders_disabled: bool | None = Field(default=None, description="Turns off Luma's default pre-event reminder emails."),
        feedback_email: dict[str, Any] | None = Field(default=None, description="{enabled, delay} settings for the post-event feedback email; delay defaults to PT0M, maximum P7D."),
        show_guest_list: bool | None = Field(default=None, description="Whether approved guests can see who else is attending."),
        slug: str | None = Field(default=None, description="URL slug for the event page (luma.com/<slug>); creation fails if unavailable."),
        tint_color: str | None = Field(default=None, description="Hex color, e.g. #bb2dc7; alpha channels are stripped."),
        visibility: str | None = Field(default=None, description="public, members-only, or private."),
        waitlist_status: str | None = Field(default=None, description="disabled or enabled — whether new registrations join a waitlist once capacity is reached."),
    ) -> EventCreateResult:
        tlog = ToolLogger(logger, "create_event")

        try:
            body = _body(
                name=name, start_at=start_at, timezone=timezone,
                can_register_for_multiple_tickets=can_register_for_multiple_tickets,
                cover_url=cover_url, coordinate=coordinate, description_md=description_md,
                end_at=end_at, geo_address_json=geo_address_json,
                location_visibility=location_visibility, max_capacity=max_capacity,
                meeting_url=meeting_url, name_requirement=name_requirement,
                phone_number_requirement=phone_number_requirement,
                registration_open=registration_open, registration_questions=registration_questions,
                reminders_disabled=reminders_disabled, feedback_email=feedback_email,
                show_guest_list=show_guest_list, slug=slug, tint_color=tint_color,
                visibility=visibility, waitlist_status=waitlist_status,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/create", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return EventCreateResult(success=True, statusCode=status, data=EventCreateData(**data))
            return _upstream_err(EventCreateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EventCreateResult, tlog, exc)

    # ------------------------------------------------------------------
    # create_ticket_type
    # ------------------------------------------------------------------
    @mcp.tool(
        name="create_ticket_type",
        description="Creates a new ticket type for an event and returns the created ticket type, including its id.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_ticket_type(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        name: str = Field(description="Ticket type name."),
        type: str = Field(description="free or paid."),
        require_approval: bool | None = Field(default=None, description="Whether registrations for this ticket type require host approval."),
        is_hidden: bool | None = Field(default=None, description="Hides the ticket type from public view, e.g. for an invite-only tier."),
        description: str | None = Field(default=None, description="Ticket type description."),
        valid_start_at: str | None = Field(default=None, description="ISO 8601 date the ticket type becomes available."),
        valid_end_at: str | None = Field(default=None, description="ISO 8601 date the ticket type stops being available."),
        max_capacity: float | None = Field(default=None, description="Maximum number of this ticket type that can be issued."),
        cents: float | None = Field(default=None, description="Ticket price as an integer in the smallest unit of currency (e.g. cents for USD); only meaningful when type is paid."),
        currency: str | None = Field(default=None, description="Currency code for cents."),
        is_flexible: bool | None = Field(default=None, description="Enables \"pay what you want\" pricing for a paid ticket."),
        min_cents: float | None = Field(default=None, description="Minimum amount a guest may pay when is_flexible is true."),
    ) -> TicketTypeCreateResult:
        tlog = ToolLogger(logger, "create_ticket_type")

        try:
            body = _body(
                event_id=event_id, name=name, type=type,
                require_approval=require_approval, is_hidden=is_hidden, description=description,
                valid_start_at=valid_start_at, valid_end_at=valid_end_at,
                max_capacity=max_capacity, cents=cents, currency=currency,
                is_flexible=is_flexible, min_cents=min_cents,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/ticket-types/create", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return TicketTypeCreateResult(success=True, statusCode=status, data=TicketTypeCreateData(**data))
            return _upstream_err(TicketTypeCreateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(TicketTypeCreateResult, tlog, exc)

    # ------------------------------------------------------------------
    # create_coupon
    # ------------------------------------------------------------------
    @mcp.tool(
        name="create_coupon",
        description="Creates a new discount coupon for an event and returns the created coupon.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_coupon(
        code: str = Field(max_length=20, description="Code the guest enters on the event page. Case-insensitive, maximum 20 characters."),
        discount: dict[str, Any] = Field(description="Discriminated union: {discount_type: \"percent\", percent_off} (0-100), or {discount_type: \"amount\", cents_off, currency}."),
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        remaining_count: int | None = Field(default=None, description="Number of times the coupon can be used. Set to 1000000 for unlimited uses."),
        valid_start_at: str | None = Field(default=None, description="ISO 8601 datetime the coupon becomes valid."),
        valid_end_at: str | None = Field(default=None, description="ISO 8601 datetime the coupon expires."),
        event_ticket_type_id: str | None = Field(default=None, description="Restrict the coupon to a single ticket type. If that ticket type is hidden, the coupon acts as an unlock/access code instead of a discount."),
    ) -> CouponCreateResult:
        tlog = ToolLogger(logger, "create_coupon")

        try:
            body = _body(
                code=code, discount=discount, event_id=event_id,
                remaining_count=remaining_count, valid_start_at=valid_start_at,
                valid_end_at=valid_end_at, event_ticket_type_id=event_ticket_type_id,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/coupons/create", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return CouponCreateResult(success=True, statusCode=status, data=CouponCreateData(**data))
            return _upstream_err(CouponCreateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CouponCreateResult, tlog, exc)

    # ------------------------------------------------------------------
    # add_guests
    # ------------------------------------------------------------------
    @mcp.tool(
        name="add_guests",
        description=(
            "Adds one or more guests directly to an event (default status \"Going\", one ticket "
            "of the default type unless overridden) and returns an empty response on success."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def add_guests(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        guests: list[dict[str, Any]] = Field(description="Guests to add, each requiring at least email; existing names are not overwritten. Each guest may include registration_answers (question_id + value) for the event's registration questions."),
        ticket: dict[str, Any] | None = Field(default=None, description="Assign a single ticket of the specified event_ticket_type_id to each guest. Cannot be combined with tickets."),
        tickets: list[dict[str, Any]] | None = Field(default=None, description="Assign multiple tickets (each by event_ticket_type_id) to each guest. Cannot be combined with ticket."),
        approval_status: str | None = Field(default=None, description="Status to assign each added guest: approved, pending_approval, or waitlist. Defaults to approved."),
        send_email: bool | None = Field(default=None, description="Whether Luma should email each added guest. Defaults to true."),
    ) -> GuestAddResult:
        tlog = ToolLogger(logger, "add_guests")

        if ticket is not None and tickets is not None:
            return _err(GuestAddResult, tlog, "VALIDATION_ERROR", "ticket and tickets cannot both be set", 400)

        try:
            body = _body(
                event_id=event_id, guests=guests, ticket=ticket, tickets=tickets,
                approval_status=approval_status, send_email=send_email,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/guests/add", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return GuestAddResult(
                    success=True, statusCode=status,
                    data=GuestAddData(event_id=event_id, guests_requested=len(guests)),
                )
            return _upstream_err(GuestAddResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GuestAddResult, tlog, exc)

    # ------------------------------------------------------------------
    # send_invites (UPDATE MANY — destructive: irreversible bulk notification, no before-state)
    # ------------------------------------------------------------------
    @mcp.tool(
        name="send_invites",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Sends one or more guests a soft invite to an event by email (and SMS if their phone "
            "is linked to their Luma account) that they can accept, returning an empty response "
            "on success. This sends real communications to every listed guest — the original "
            "invite state is not returned and cannot be recovered from this call. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly which guests will be invited and what the "
            "message will say, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def send_invites(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        guests: list[dict[str, Any]] = Field(description="Guests to invite, each requiring at least email; existing names are not overwritten."),
        message: str | None = Field(default=None, max_length=200, description="Personalized message included in the invite. Maximum 200 characters."),
    ) -> InviteSendResult:
        tlog = ToolLogger(logger, "send_invites")

        try:
            body = _body(event_id=event_id, guests=guests, message=message)
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/guests/send-invites", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return InviteSendResult(
                    success=True, statusCode=status,
                    data=InviteSendData(event_id=event_id, guests_invited=len(guests)),
                )
            return _upstream_err(InviteSendResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(InviteSendResult, tlog, exc)

    # ------------------------------------------------------------------
    # cancel_event (DELETE — destructive)
    # ------------------------------------------------------------------
    @mcp.tool(
        name="cancel_event",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Cancels an event using a cancellation token from request_event_cancellation and "
            "returns an empty response on success. This action is irreversible — the event is "
            "deleted, all guests are notified, and refunds are processed if requested; the event "
            "cannot be recovered after this call. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what event will be permanently cancelled and "
            "that it is irreversible, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def cancel_event(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        cancellation_token: str = Field(description="The cancellation token returned by request_event_cancellation."),
        should_refund: bool | None = Field(default=None, description="Whether to refund paid guests. Conditionally required — must be set if the event has paid guests (see is_paid from request_event_cancellation)."),
    ) -> EventCancelResult:
        tlog = ToolLogger(logger, "cancel_event")

        try:
            body = _body(
                event_id=event_id, cancellation_token=cancellation_token,
                should_refund=should_refund,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/cancel", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return EventCancelResult(success=True, statusCode=status, data=EventCancelData(event_id=event_id))
            return _upstream_err(EventCancelResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EventCancelResult, tlog, exc)

    # ------------------------------------------------------------------
    # update_event (UPDATE — API returns an empty body, so no "after" resource is available;
    # returns a confirmation of what was sent instead of a fabricated after-state. Call
    # get_event afterward to see the resulting state.)
    # ------------------------------------------------------------------
    @mcp.tool(
        name="update_event",
        description=(
            "Updates an existing event's details. Only the fields you provide are changed — "
            "others keep their current value. NOTE: this overwrites the current field values — "
            "the API does not return the updated event, and the original state is not preserved "
            "after the call, so the response is a confirmation of the fields that were sent "
            "rather than a before/after snapshot. Call get_event afterward to see the resulting state."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_event(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        suppress_notifications: bool | None = Field(default=None, description="If true, guests are not notified (email/push) when the name, time, or location changes."),
        can_register_for_multiple_tickets: bool | None = Field(default=None, description="Whether a single guest can register for multiple tickets."),
        cover_url: str | None = Field(default=None, description="Cover image URL; must be hosted on the Luma CDN (images.lumacdn.com)."),
        coordinate: dict[str, Any] | None = Field(default=None, description="{longitude, latitude} for the event location."),
        description_md: str | None = Field(default=None, description="Markdown description, converted internally to Luma's rich text format."),
        end_at: str | None = Field(default=None, description="ISO 8601 datetime the event ends."),
        geo_address_json: dict[str, Any] | None = Field(default=None, description="Either {type: \"manual\", address} or {type: \"google\", place_id, description?}."),
        location_visibility: str | None = Field(default=None, description="public (default) or guests-only."),
        max_capacity: float | None = Field(default=None, description="Maximum registrations before the event is marked sold out (or joins the waitlist, if enabled)."),
        meeting_url: str | None = Field(default=None, description="Virtual meeting URL for online events."),
        name: str | None = Field(default=None, description="Event name."),
        name_requirement: str | None = Field(default=None, description="full-name or first-last."),
        phone_number_requirement: str | None = Field(default=None, description="optional or required; omit to not collect it."),
        registration_open: bool | None = Field(default=None, description="Whether to accept registrations."),
        registration_questions: list[dict[str, Any]] | None = Field(default=None, description="Custom registration questions; each object is discriminated by question_type."),
        reminders_disabled: bool | None = Field(default=None, description="Turns off Luma's default pre-event reminder emails."),
        feedback_email: dict[str, Any] | None = Field(default=None, description="{enabled, delay} settings for the post-event feedback email."),
        show_guest_list: bool | None = Field(default=None, description="Whether approved guests can see who else is attending."),
        slug: str | None = Field(default=None, description="URL slug for the event page; update fails if unavailable."),
        start_at: str | None = Field(default=None, description="ISO 8601 datetime the event starts."),
        timezone: str | None = Field(default=None, description="IANA timezone, e.g. America/New_York."),
        tint_color: str | None = Field(default=None, description="Hex color; alpha channels are stripped."),
        visibility: str | None = Field(default=None, description="public, members-only, or private."),
        waitlist_status: str | None = Field(default=None, description="disabled or enabled."),
    ) -> EventUpdateResult:
        tlog = ToolLogger(logger, "update_event")

        try:
            body = _body(
                event_id=event_id, suppress_notifications=suppress_notifications,
                can_register_for_multiple_tickets=can_register_for_multiple_tickets,
                cover_url=cover_url, coordinate=coordinate, description_md=description_md,
                end_at=end_at, geo_address_json=geo_address_json,
                location_visibility=location_visibility, max_capacity=max_capacity,
                meeting_url=meeting_url, name=name, name_requirement=name_requirement,
                phone_number_requirement=phone_number_requirement,
                registration_open=registration_open, registration_questions=registration_questions,
                reminders_disabled=reminders_disabled, feedback_email=feedback_email,
                show_guest_list=show_guest_list, slug=slug, start_at=start_at,
                timezone=timezone, tint_color=tint_color, visibility=visibility,
                waitlist_status=waitlist_status,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/update", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                updated_fields = sorted(k for k in body if k != "event_id")
                return EventUpdateResult(
                    success=True, statusCode=status,
                    data=EventUpdateData(event_id=event_id, updated_fields=updated_fields),
                )
            return _upstream_err(EventUpdateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(EventUpdateResult, tlog, exc)

    # ------------------------------------------------------------------
    # update_guest_status (UPDATE — API returns an empty body; see update_event note.)
    # ------------------------------------------------------------------
    @mcp.tool(
        name="update_guest_status",
        description=(
            "Updates a guest's status (approved, declined, pending_approval, or waitlist), "
            "optionally refunding them and/or emailing a personal message. NOTE: this overwrites "
            "the guest's current status — the API does not return the updated guest, and the "
            "original status is not preserved after the call, so the response is a confirmation "
            "of the change that was sent rather than a before/after snapshot. Call get_guest "
            "afterward to see the resulting state."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_guest_status(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        guest_id: str = Field(description="Guest identifier — the guest ID (gst-), a ticket key, a guest key (g-), or the user's email."),
        status: str = Field(description="approved, declined, pending_approval, or waitlist."),
        should_refund: bool | None = Field(default=None, description="If moving a paid guest to declined, waitlist, or pending_approval, whether to refund their payment. Defaults to false."),
        send_email: bool | None = Field(default=None, description="Whether Luma should email the guest about the status change. Defaults to true."),
        message: str | None = Field(default=None, max_length=200, description="Personal message included in the status-change email. Maximum 200 characters. Can't be combined with send_email: false."),
    ) -> GuestStatusUpdateResult:
        tlog = ToolLogger(logger, "update_guest_status")

        if message is not None and send_email is False:
            return _err(GuestStatusUpdateResult, tlog, "VALIDATION_ERROR", "message cannot be combined with send_email: false", 400)

        try:
            body = _body(
                event_id=event_id, guest_id=guest_id, status=status,
                should_refund=should_refund, send_email=send_email, message=message,
            )
            data, status_code, retry_after = service.api_request(
                "POST", "/v1/events/guests/update-status", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status_code < 300:
                tlog.success()
                return GuestStatusUpdateResult(
                    success=True, statusCode=status_code,
                    data=GuestStatusUpdateData(event_id=event_id, guest_id=guest_id, status=status),
                )
            return _upstream_err(GuestStatusUpdateResult, tlog, status_code, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GuestStatusUpdateResult, tlog, exc)

    # ------------------------------------------------------------------
    # update_guest_tickets (UPDATE — API returns an empty body; see update_event note.)
    # ------------------------------------------------------------------
    @mcp.tool(
        name="update_guest_tickets",
        description=(
            "Administratively adds complimentary tickets to or removes/invalidates tickets from "
            "an existing guest with no payment or refund processed. NOTE: this overwrites the "
            "guest's ticket set — the API does not return the updated guest, and the original "
            "ticket set is not preserved after the call, so the response is a confirmation of "
            "the tickets added/removed rather than a before/after snapshot. Call get_guest "
            "afterward to see the resulting state."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_guest_tickets(
        event_id: str = Field(description="Event ID, this usually starts with evt-."),
        guest_id: str = Field(description="Guest identifier — the guest ID (gst-), a ticket key, a guest key (g-), or the user's email."),
        ticket_ids_to_remove: list[str] | None = Field(default=None, description="Existing ticket IDs to invalidate. Removing tickets does not issue a refund, and at least one valid ticket must remain on the guest. Default []."),
        tickets_to_add: list[dict[str, Any]] | None = Field(default=None, description="Complimentary tickets to grant (each by event_ticket_type_id); each entry creates a new $0 administrative ticket even for a normally paid ticket type. Default []."),
        send_email: bool | None = Field(default=None, description="Whether Luma may email the guest about the ticket change. Defaults to true and still respects notification preferences."),
    ) -> GuestTicketUpdateResult:
        tlog = ToolLogger(logger, "update_guest_tickets")

        try:
            body = _body(
                event_id=event_id, guest_id=guest_id,
                ticket_ids_to_remove=ticket_ids_to_remove, tickets_to_add=tickets_to_add,
                send_email=send_email,
            )
            data, status, retry_after = service.api_request(
                "POST", "/v1/events/guests/update-tickets", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return GuestTicketUpdateResult(
                    success=True, statusCode=status,
                    data=GuestTicketUpdateData(
                        event_id=event_id, guest_id=guest_id,
                        tickets_added=len(tickets_to_add) if tickets_to_add else 0,
                        tickets_removed=len(ticket_ids_to_remove) if ticket_ids_to_remove else 0,
                    ),
                )
            return _upstream_err(GuestTicketUpdateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GuestTicketUpdateResult, tlog, exc)

    # ------------------------------------------------------------------
    # update_ticket_type (UPDATE — the API does return the updated ticket type, so a real
    # before/after pair is captured: "before" via a discovery call to the get_ticket_type
    # endpoint, "after" from the update response.)
    # ------------------------------------------------------------------
    @mcp.tool(
        name="update_ticket_type",
        description=(
            "Updates an existing ticket type's details and returns the updated ticket type. "
            "Only the fields you provide are changed — others keep their current value. "
            "NOTE: this overwrites the current field values — the original state is not stored "
            "after the call. The response includes both the before and after state so you have "
            "a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_ticket_type(
        event_ticket_type_id: str = Field(description="Ticket type ID, this usually starts with ttype-."),
        name: str | None = Field(default=None, description="Ticket type name."),
        require_approval: bool | None = Field(default=None, description="Whether registrations for this ticket type require host approval."),
        is_hidden: bool | None = Field(default=None, description="Hides the ticket type from public view."),
        description: str | None = Field(default=None, description="Ticket type description."),
        valid_start_at: str | None = Field(default=None, description="ISO 8601 date the ticket type becomes available."),
        valid_end_at: str | None = Field(default=None, description="ISO 8601 date the ticket type stops being available."),
        max_capacity: float | None = Field(default=None, description="Maximum number of this ticket type that can be issued."),
        type: str | None = Field(default=None, description="free or paid."),
        cents: float | None = Field(default=None, description="Ticket price as an integer in the smallest unit of currency; only meaningful when type is paid."),
        currency: str | None = Field(default=None, description="Currency code for cents."),
        is_flexible: bool | None = Field(default=None, description="Enables \"pay what you want\" pricing for a paid ticket."),
        min_cents: float | None = Field(default=None, description="Minimum amount a guest may pay when is_flexible is true."),
    ) -> TicketTypeUpdateResult:
        tlog = ToolLogger(logger, "update_ticket_type")

        try:
            before_data, before_status, before_retry_after = service.api_request(
                "GET", "/v1/events/ticket-types/get",
                params={"event_ticket_type_id": event_ticket_type_id},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if not (200 <= before_status < 300):
                return _upstream_err(TicketTypeUpdateResult, tlog, before_status, before_data, before_retry_after)
            before = TicketTypeData(**before_data)

            body = _body(
                event_ticket_type_id=event_ticket_type_id, name=name,
                require_approval=require_approval, is_hidden=is_hidden, description=description,
                valid_start_at=valid_start_at, valid_end_at=valid_end_at,
                max_capacity=max_capacity, type=type, cents=cents, currency=currency,
                is_flexible=is_flexible, min_cents=min_cents,
            )
            after_data, status, retry_after = service.api_request(
                "POST", "/v1/events/ticket-types/update", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                after = TicketTypeData(**after_data)
                return TicketTypeUpdateResult(
                    success=True, statusCode=status,
                    data=TicketTypeUpdateData(before=before, after=after),
                )
            return _upstream_err(TicketTypeUpdateResult, tlog, status, after_data, retry_after)
        except Exception as exc:
            return _handle_request_exc(TicketTypeUpdateResult, tlog, exc)
