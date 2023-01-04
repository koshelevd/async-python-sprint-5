from settings.api import api_settings

type_sorted_asc = "asc"
type_sorted_desc = "desc"


def get_short_url(short_id: int) -> str:
    """Get short url by short id."""
    return (
        f"http://{api_settings.SERVER_HOST}:"
        f"{api_settings.SERVER_PORT}/{short_id}"
    )
