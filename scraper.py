from httpx import Client
from parsel import Selector





REGIONS = ["Burgenland", "Kaernten",
           "Niederoesterreich",
           "Oberoesterreich",
           "Salzburg", "Steiermark",
            "Tirol", "Vorarlberg", "Wien"
           ]


def main(flat_type: str = None, contract_type: str = None, page_count: int = 1):

    seed = "https://www.immmo.at/immo"
    contract = contract_factory(flat_type, contract_type)
    for region in REGIONS:
        start_url = seed + contract + f"/{region}"
        print("------------------------------------------------------------------------------------------")
        print(f"{region}  {contract}  category_url: {start_url}")
        print("------------------------------------------------------------------------------------------")
        scrape_category(start_url, page_count)


def scrape_category(start_url, page_count):
    with Client(timeout=10, follow_redirects=True) as session:
        index = 1
        while True:
            req = session.get(start_url + "/" + str(index))
            if req.status_code != 200:
                break
            parse(Selector(text=req.text))
            index += 1
            if index > page_count:
                break


def parse(response: Selector):

    items = response.xpath("//li[@class='wrapper-result']")
    for item in items:
        realestate_uid = item.xpath("./@data-realestateuid").get()
        host = item.xpath("./@data-hostname").get()
        host_id = item.xpath("./@data-hostuid").get()
        texts = item.xpath(".//text()")
        text_box = None
        for text in texts:
            if not text_box:
                text_box = text.get()
            else:
                text_box += text.get()
        print("----------------------------------------------------------------------------------------------")
        print(f"host: {host}  host_id: {host_id}   realestate_uid: {realestate_uid}")
        print(text_box)


def contract_factory(flat_type: str = None, contract_type: str = None):
    """factory to advance the url in case contract filters are required"""
    flat_type_definitions = {"house": "Haus",
                             "apartment": "Wohnung"
                             }
    contract_type_definitions = {"buy": "kaufen",
                                 "rent": "mieten"
                                 }
    # default
    if not isinstance(flat_type, str):
        return "/Immobilie"

    # guard to make sure settings are correct
    if isinstance(contract_type, str) and contract_type.lower() not in ["buy", "rent"]:
        raise Exception("contract_type must be either buy or rent")
    if isinstance(flat_type, str) and flat_type.lower() not in ["house", "apartment"]:
        raise Exception("flat_type must be either house or apartment")

    # construct url
    f_choice = flat_type_definitions.get(flat_type.lower()) if isinstance(flat_type, str) else None
    c_choice = contract_type_definitions.get(contract_type.lower()) if isinstance(contract_type, str) else None
    ep = f"/{f_choice}"
    if c_choice is not None:
        ep += f"-{c_choice}"
    return ep


if __name__ == '__main__':
    # main(flat_type="house", page_count=5)
    main(page_count=2)



