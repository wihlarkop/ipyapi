"""Example usage of ipyapi library."""

import asyncio

from ipyapi import AsyncIPyAPI, IPyAPI


def sync_example():
    """Example of synchronous usage."""
    print("=== Synchronous Example ===\n")

    with IPyAPI() as client:
        # Get complete location data
        location = client.get_location("8.8.8.8")
        print(f"IP: {location.ip}")
        print(f"Location: {location.city}, {location.country_name}")
        print(f"Coordinates: {location.latitude}, {location.longitude}")
        print(f"Timezone: {location.timezone}")
        print(f"ISP: {location.org}")
        print()

        # Get specific fields
        country = client.get_country("1.1.1.1")
        print(f"1.1.1.1 is from: {country}")
        print()

        # Get your own IP
        my_ip = client.get_ip()
        print(f"Your IP: {my_ip}")
        print()


async def async_example():
    """Example of asynchronous usage."""
    print("=== Asynchronous Example ===\n")

    async with AsyncIPyAPI() as client:
        # Get multiple IPs concurrently
        tasks = [
            client.get_location("8.8.8.8"),
            client.get_location("1.1.1.1"),
            client.get_location("208.67.222.222"),
        ]

        locations = await asyncio.gather(*tasks)

        for location in locations:
            print(f"{location.ip} - {location.city}, {location.country_name} ({location.org})")


if __name__ == "__main__":
    # Run synchronous example
    sync_example()

    # Run async example
    asyncio.run(async_example())
