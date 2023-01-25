"""Class View."""


class View:
    """The view is an event that includes userId, movieId and sequence number of the frame."""

    def __init__(
        self, id: int = 0, user_id: str = "", movie_id: str = "", viewed_frame: int = 0
    ):
        self.id = id
        self.user_id = user_id
        self.movie_id = movie_id
        self.viewed_frame = viewed_frame

    def __str__(self):
        return f"{self.user_id} -- {self.movie_id} - {self.viewed_frame}"
