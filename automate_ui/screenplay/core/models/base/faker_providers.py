from typing import Dict

from faker.providers import BaseProvider
import pycountry


class CountrySpecificProvider(BaseProvider):
    """Custom Faker provider for country-specific data."""

    def country_state(self, country: str) -> str:
        """Get a state/province for a specific country using pycountry."""
        try:
            country_obj = pycountry.countries.get(name=country)
            if not country_obj:
                return self.generator.state()

            subdivisions = list(
                pycountry.subdivisions.get(country_code=country_obj.alpha_2)
            )
            if not subdivisions:
                return self.generator.state()

            valid_subdivisions = [
                sub
                for sub in subdivisions
                if not any(
                    x in sub.name.lower() for x in ["unknown", "other", "unassigned"]
                )
            ]

            if not valid_subdivisions:
                return self.generator.state()

            return self.generator.random_element(valid_subdivisions).name
        except Exception:
            # Fallback to Faker's state if pycountry fails
            return self.generator.state()

    def country_postal_code(self, country: str) -> str:
        """Get a postal code for a specific country."""
        try:
            country_obj = pycountry.countries.get(name=country)
            if not country_obj:
                return self.generator.postcode()

            country_code = country_obj.alpha_2

            # Define postal code patterns by country
            patterns = {
                "CA": lambda: f"{self.generator.random_letter().upper()}{self.generator.random_number(digits=1)}"
                f"{self.generator.random_letter().upper()} {self.generator.random_number(digits=1)}"
                f"{self.generator.random_letter().upper()}{self.generator.random_number(digits=1)}",
                "AU": lambda: str(self.generator.random_number(digits=4)),
                "US": lambda: f"{self.generator.random_number(digits=5)}"
                + (
                    f"-{self.generator.random_number(digits=4)}"
                    if self.generator.boolean(chance_of_getting_true=30)
                    else ""
                ),
                "GB": lambda: f"{self.generator.random_letter().upper()}{self.generator.random_letter().upper()}"
                f"{self.generator.random_number(digits=1)}"
                f"{self.generator.random_letter().upper() if self.generator.boolean(chance_of_getting_true=30) else ''} "
                f"{self.generator.random_number(digits=1)}"
                f"{self.generator.random_letter().upper()}{self.generator.random_letter().upper()}",
            }

            pattern = patterns.get(country_code, lambda: self.generator.postcode())
            return pattern()

        except Exception:
            return self.generator.postcode()

    def county(self) -> str:
        """Get a random county name."""
        counties = [
            "Adams",
            "Allen",
            "Anderson",
            "Andrews",
            "Angelina",
            "Aransas",
            "Archer",
            "Armstrong",
            "Atascosa",
            "Austin",
            "Bailey",
            "Bandera",
            "Bastrop",
            "Baylor",
            "Bee",
            "Bell",
            "Bexar",
            "Blanco",
            "Borden",
            "Bosque",
            "Bowie",
            "Brazoria",
            "Brazos",
            "Brewster",
            "Briscoe",
            "Brooks",
            "Brown",
            "Burleson",
            "Burnet",
            "Caldwell",
            "Calhoun",
            "Callahan",
            "Cameron",
            "Camp",
            "Carson",
            "Cass",
            "Castro",
            "Chambers",
            "Cherokee",
            "Childress",
            "Clay",
            "Cochran",
            "Coke",
            "Coleman",
            "Collin",
            "Collingsworth",
            "Colorado",
            "Comal",
            "Comanche",
            "Concho",
            "Cooke",
            "Coryell",
            "Cottle",
            "Crane",
            "Crockett",
            "Crosby",
            "Culberson",
            "Dallam",
            "Dallas",
            "Dawson",
            "Deaf Smith",
            "Delta",
            "Denton",
            "DeWitt",
            "Dickens",
            "Dimmit",
            "Donley",
            "Duval",
            "Eastland",
            "Ector",
            "Edwards",
            "El Paso",
            "Ellis",
            "Erath",
            "Falls",
            "Fannin",
            "Fayette",
            "Fisher",
            "Floyd",
            "Foard",
            "Fort Bend",
            "Franklin",
            "Freestone",
            "Frio",
            "Gaines",
            "Galveston",
            "Garza",
            "Gillespie",
            "Glasscock",
            "Goliad",
            "Gonzales",
            "Gray",
            "Grayson",
            "Gregg",
            "Grimes",
            "Guadalupe",
            "Hale",
            "Hall",
            "Hamilton",
            "Hansford",
            "Hardeman",
            "Hardin",
            "Harris",
            "Harrison",
            "Hartley",
            "Haskell",
            "Hays",
            "Hemphill",
            "Henderson",
            "Hidalgo",
            "Hill",
            "Hockley",
            "Hood",
            "Hopkins",
            "Houston",
            "Howard",
            "Hudspeth",
            "Hunt",
            "Hutchinson",
            "Irion",
            "Jack",
            "Jackson",
            "Jasper",
            "Jeff Davis",
            "Jefferson",
            "Jim Hogg",
            "Jim Wells",
            "Johnson",
            "Jones",
            "Karnes",
            "Kaufman",
            "Kendall",
            "Kenedy",
            "Kent",
            "Kerr",
            "Kimble",
            "King",
            "Kinney",
            "Kleberg",
            "Knox",
            "La Salle",
            "Lamar",
            "Lamb",
            "Lampasas",
            "Lavaca",
            "Lee",
            "Leon",
            "Liberty",
            "Limestone",
            "Lipscomb",
            "Live Oak",
            "Llano",
            "Loving",
            "Lubbock",
            "Lynn",
            "Madison",
            "Marion",
            "Martin",
            "Mason",
            "Matagorda",
            "Maverick",
            "McCulloch",
            "McLennan",
            "McMullen",
            "Medina",
            "Menard",
            "Midland",
            "Milam",
            "Mills",
            "Mitchell",
            "Montague",
            "Montgomery",
            "Moore",
            "Morris",
            "Motley",
            "Nacogdoches",
            "Navarro",
            "Newton",
            "Nolan",
            "Nueces",
            "Ochiltree",
            "Oldham",
            "Orange",
            "Palo Pinto",
            "Panola",
            "Parker",
            "Parmer",
            "Pecos",
            "Polk",
            "Potter",
            "Presidio",
            "Rains",
            "Randall",
            "Reagan",
            "Real",
            "Red River",
            "Reeves",
            "Refugio",
            "Roberts",
            "Robertson",
            "Rockwall",
            "Runnels",
            "Rusk",
            "Sabine",
            "San Augustine",
            "San Jacinto",
            "San Patricio",
            "San Saba",
            "Schleicher",
            "Scurry",
            "Shackelford",
            "Shelby",
            "Sherman",
            "Smith",
            "Somervell",
            "Starr",
            "Stephens",
            "Sterling",
            "Stonewall",
            "Sutton",
            "Swisher",
            "Tarrant",
            "Taylor",
            "Terrell",
            "Terry",
            "Throckmorton",
            "Titus",
            "Tom Green",
            "Travis",
            "Trinity",
            "Tyler",
            "Upshur",
            "Upton",
            "Uvalde",
            "Val Verde",
            "Van Zandt",
            "Victoria",
            "Walker",
            "Waller",
            "Ward",
            "Washington",
            "Webb",
            "Wharton",
            "Wheeler",
            "Wichita",
            "Wilbarger",
            "Willacy",
            "Williamson",
            "Wilson",
            "Winkler",
            "Wise",
            "Wood",
            "Yoakum",
            "Young",
            "Zapata",
            "Zavala",
        ]
        return self.generator.random_element(counties)


class PhoneNumberGenerator:
    """Utility class for generating phone numbers based on country format."""

    COUNTRY_CODES: Dict[str, str] = {
        "Canada": "+1",
        "United States": "+1",
        "Australia": "+61",
        "United Kingdom": "+44",
        "New Zealand": "+64",
        "Singapore": "+65",
    }

    @classmethod
    def generate_phone_number(cls, faker, country: str = "Canada") -> str:
        """Generate a phone number based on country format.

        Args:
            faker: Faker instance to use for random number generation
            country: The country to generate the phone number for. Defaults to Canada.

        Returns:
            A formatted phone number string with country code.
        """
        country_code = cls.COUNTRY_CODES.get(
            country, "+1"
        )  # Default to +1 if country not found

        if country in ["Canada", "United States"]:
            # North American format: +1XXXXXXXXXX
            # Valid area codes for Canada and US (not exhaustive)
            valid_area_codes = [
                "204",
                "226",
                "236",
                "249",
                "250",
                "289",
                "306",
                "343",
                "365",
                "367",
                "403",
                "416",
                "418",
                "431",
                "437",
                "438",
                "450",
                "506",
                "514",
                "519",
                "548",
                "579",
                "581",
                "587",
                "604",
                "613",
                "639",
                "647",
                "705",
                "709",
                "778",
                "780",
                "782",
                "807",
                "819",
                "825",
                "867",
                "873",
                "902",
                "905",
                "201",
                "202",
                "203",
                "205",
                "206",
                "207",
                "208",
                "209",
                "210",
                "212",
                "213",
                "214",
                "215",
                "216",
                "217",
                "218",
                "219",
                "220",
                "224",
                "225",
                "228",
                "229",
                "231",
                "234",
                "239",
                "240",
                "248",
                "251",
                "252",
                "253",
            ]
            area_code = faker.random_element(valid_area_codes)
            prefix = faker.random_number(digits=3, fix_len=True)
            line = faker.random_number(digits=4, fix_len=True)

            return f"{country_code}{area_code}{prefix}{line}"
        elif country == "Australia":
            # Australian format: +61XXXXXXXXX
            mobile_prefix = "4"  # Australian mobile numbers start with 4
            remaining_digits = faker.random_number(digits=8, fix_len=True)
            return f"{country_code}{mobile_prefix}{remaining_digits}"
        elif country == "United Kingdom":
            # UK format: +44XXXXXXXXXX
            mobile_prefix = "7"  # UK mobile numbers start with 7
            remaining_digits = faker.random_number(digits=9, fix_len=True)
            return f"{country_code}{mobile_prefix}{remaining_digits}"
        elif country == "Singapore":
            # Singapore format: +65XXXXXXXX
            mobile_prefix = "8"  # Singapore mobile numbers start with 8 or 9
            remaining_digits = faker.random_number(digits=7, fix_len=True)
            return f"{country_code}{mobile_prefix}{remaining_digits}"
        else:
            return f"{country_code}{faker.random_number(digits=10, fix_len=True)}"
