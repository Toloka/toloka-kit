__all__ = [
    'User',
]

from typing import List

from .primitives.base import BaseTolokaObject


class User(BaseTolokaObject):
    """Information about a Toloker.

    It contains information specified in the Toloker's profile and information about the Toloker's device.

    Attributes:
        id: The Toloker's ID.
        country: The country code.
        languages: A list of languages specified in the profile.
        adult_allowed: An option showing whether the Toloker agrees to complete tasks with adult content.
        attributes: Toloker's device and software attributes.
    """

    class Attributes(BaseTolokaObject):
        """Toloker's device and software attributes.

        Attributes:
            country_by_phone: A [two-letter country code](https://toloka.ai/docs/api/regions) determined by the phone number.
            country_by_ip: A [two-letter country code] (https://toloka.ai/docs/api/regions) determined by the IP address.
            client_type: A Toloker's client:
                * `TOLOKA_APP` — A mobile application.
                * `BROWSER` — A browser.
            user_agent_type: A user agent type which the client application uses to identify itself.
                * `BROWSER` — A desktop browser.
                * `MOBILE_BROWSER` — A mobile browser.
                * `OTHER` — User agents which could not be identified as either desktop or mobile browsers. Normally, the Toloka mobile application identifies itself as `OTHER`.
            device_category: The category of the Toloker's device.
                * `PERSONAL_COMPUTER` — A personal computer.
                * `SMARTPHONE` — A smartphone.
                * `TABLET` — A tablet device.
                * `WEARABLE_COMPUTER` — A wearable device, such as a smart watch.
            os_family: The operating system family installed on the device.
                * `ANDROID` — Android.
                * `BLACKBERRY` — BlackBerry OS.
                * `BSD` — BSD OS, like FreeBSD, OpenBSD, NetBSD, or DragonFly BSD.
                * `IOS` — iOS.
                * `LINUX` — An OS based on the Linux kernel.
                * `MAC_OS` — Classic Mac OS.
                * `OS_X` — macOS.
                * `WINDOWS` — Windows OS.
            os_version: The version of the OS.
                The version consists of major and minor version numbers, for example, `14.4`.
            os_version_major: The major version of the OS.
            os_version_minor: The minor version of the OS.
            os_version_bugfix: The build number or the bugfix version of the OS.

        """

        country_by_phone: str
        country_by_ip: str
        client_type: str
        user_agent_type: str
        device_category: str
        os_family: str
        os_version: float
        os_version_major: int
        os_version_minor: int
        os_version_bugfix: int

    id: str
    country: str
    languages: List[str]
    adult_allowed: bool
    attributes: Attributes
