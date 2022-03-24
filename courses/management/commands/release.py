import subprocess

from django.core.management.base import BaseCommand
from learn_music.settings import BASE_DIR


class Command(BaseCommand):

    help = "Helper script to manage versioning"

    def add_arguments(self, parser):
        parser.add_argument("ver", type=str, help="version")

    def handle(self, *args, **options):

        try:
            with open(BASE_DIR / "version.txt") as f:
                old_ver = f.read().strip()
        except:
            old_ver = "0.0.0"

        version_numbers = [int(v) for v in old_ver.split(".")]

        if options["ver"] == "major":
            version_numbers[0] = version_numbers[0] + 1
            version_numbers[1] = 0
            version_numbers[2] = 0
        elif options["ver"] == "minor":
            version_numbers[1] = version_numbers[1] + 1
            version_numbers[2] = 0
        elif options["ver"] == "patch":
            version_numbers[2] = version_numbers[2] + 1
        else:
            raise ValueError("Invalid release type")

        new_ver = ".".join([str(v) for v in version_numbers])

        self.stdout.write(f"upgrading {old_ver} to {new_ver}")

        with open(BASE_DIR / "version.txt", "w") as f:
            f.write(f"{new_ver}\n")

        subprocess.call(["git", "add", "version.txt"])
        subprocess.call(["git", "commit", "-m", new_ver])
        subprocess.call(["git", "tag", f"v{new_ver}"])

        subprocess.call(["git", "push"])
        subprocess.call(["git", "push", "--tags"])

        self.stdout.write(self.style.SUCCESS("Done"))
