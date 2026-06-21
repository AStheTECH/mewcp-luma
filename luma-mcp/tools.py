from pydantic import Field
from fastmcp import FastMCP
from service import make_luma_request

_ASPECT_RATIOS = "Options: '16:9', '9:16', '4:3', '3:4', '21:9', '9:21'."


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_text_to_video",
        description=(
            "Generate a video from a text prompt using Luma Dream Machine. "
            "Returns a generation ID and initial state. "
            "Use get_generation to poll for completion and retrieve the video URL."
        ),
    )
    def create_text_to_video(
        prompt: str = Field(
            ...,
            description="Text description of the video to generate. Be detailed — describe action, style, lighting, and camera movement for best results.",
            max_length=2000,
        ),
        loop: bool = Field(
            False,
            description="Set to true to produce a seamlessly looping video.",
        ),
        aspect_ratio: str = Field(
            "16:9",
            description=f"Aspect ratio of the output video. {_ASPECT_RATIOS}",
        ),
    ) -> dict:
        valid_ratios = {"16:9", "9:16", "4:3", "3:4", "21:9", "9:21"}
        if aspect_ratio not in valid_ratios:
            return {"error": f"Invalid aspect_ratio '{aspect_ratio}'. {_ASPECT_RATIOS}"}
        if not prompt.strip():
            return {"error": "prompt must not be empty"}

        result = make_luma_request(
            "POST",
            "generations",
            body={"prompt": prompt, "loop": loop, "aspect_ratio": aspect_ratio},
        )
        if "error" in result:
            return result
        return {
            "id": result.get("id"),
            "state": result.get("state"),
            "prompt": result.get("prompt"),
            "created_at": result.get("created_at"),
        }

    @mcp.tool(
        name="create_image_to_video",
        description=(
            "Generate a video using a starting image as the first frame. "
            "Optionally provide an end image and a text prompt to guide motion. "
            "Returns a generation ID — poll get_generation for the video URL."
        ),
    )
    def create_image_to_video(
        start_image_url: str = Field(
            ...,
            description="Publicly accessible URL of the image to use as the first frame.",
        ),
        prompt: str = Field(
            "",
            description="Optional text prompt describing the motion or scene. Leave blank to animate the image naturally.",
            max_length=2000,
        ),
        end_image_url: str = Field(
            "",
            description="Optional publicly accessible URL for the last frame. Luma will interpolate between start and end.",
        ),
        loop: bool = Field(
            False,
            description="Set to true to produce a seamlessly looping video.",
        ),
        aspect_ratio: str = Field(
            "16:9",
            description=f"Aspect ratio of the output video. {_ASPECT_RATIOS}",
        ),
    ) -> dict:
        valid_ratios = {"16:9", "9:16", "4:3", "3:4", "21:9", "9:21"}
        if aspect_ratio not in valid_ratios:
            return {"error": f"Invalid aspect_ratio '{aspect_ratio}'. {_ASPECT_RATIOS}"}
        if not start_image_url.strip():
            return {"error": "start_image_url must not be empty"}

        keyframes: dict = {"frame0": {"type": "image", "url": start_image_url.strip()}}
        if end_image_url.strip():
            keyframes["frame1"] = {"type": "image", "url": end_image_url.strip()}

        body: dict = {
            "loop": loop,
            "aspect_ratio": aspect_ratio,
            "keyframes": keyframes,
        }
        if prompt.strip():
            body["prompt"] = prompt.strip()

        result = make_luma_request("POST", "generations", body=body)
        if "error" in result:
            return result
        return {
            "id": result.get("id"),
            "state": result.get("state"),
            "prompt": result.get("prompt"),
            "created_at": result.get("created_at"),
        }

    @mcp.tool(
        name="get_generation",
        description=(
            "Get the status and result of a Luma video generation by ID. "
            "State values: 'queued' (waiting), 'dreaming' (rendering), "
            "'completed' (done — assets.video has the URL), 'failed' (see failure_reason)."
        ),
    )
    def get_generation(
        generation_id: str = Field(
            ...,
            description="The generation ID returned by create_text_to_video or create_image_to_video.",
        ),
    ) -> dict:
        if not generation_id.strip():
            return {"error": "generation_id must not be empty"}
        return make_luma_request("GET", f"generations/{generation_id.strip()}")

    @mcp.tool(
        name="list_generations",
        description=(
            "List Luma video generations ordered by creation time, newest first. "
            "Includes state and video URL for completed generations."
        ),
    )
    def list_generations(
        limit: int = Field(
            10,
            description="Maximum number of generations to return (1–100).",
            ge=1,
            le=100,
        ),
        offset: int = Field(
            0,
            description="Number of generations to skip for pagination.",
            ge=0,
        ),
    ) -> dict:
        return make_luma_request(
            "GET", "generations", params={"limit": limit, "offset": offset}
        )

    @mcp.tool(
        name="delete_generation",
        description=(
            "Permanently delete a Luma video generation by ID. "
            "This cannot be undone — the video asset will no longer be accessible."
        ),
    )
    def delete_generation(
        generation_id: str = Field(
            ...,
            description="The generation ID to delete.",
        ),
    ) -> dict:
        if not generation_id.strip():
            return {"error": "generation_id must not be empty"}
        return make_luma_request("DELETE", f"generations/{generation_id.strip()}")

    @mcp.tool(
        name="list_camera_motions",
        description=(
            "List the supported camera motion types for Luma Dream Machine "
            "(e.g., 'camera orbit left', 'camera push in', 'camera crane up'). "
            "Reference these in your text prompt to control camera behavior."
        ),
    )
    def list_camera_motions() -> dict:
        return make_luma_request("GET", "generations/camera-motion/list")

    @mcp.tool(
        name="health",
        description="Check that the MewCP Luma server is running and the API credential is accepted by Luma.",
    )
    def health() -> dict:
        result = make_luma_request("GET", "generations", params={"limit": 1})
        if "error" in result:
            return {
                "status": "unhealthy",
                "error": result["error"],
                "status_code": result.get("status_code"),
                "raw": result.get("raw"),
            }
        return {"status": "healthy", "server": "MewCP Luma MCP Server"}
