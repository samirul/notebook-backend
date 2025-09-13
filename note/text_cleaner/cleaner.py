import re
from bs4 import BeautifulSoup
import html

class CleanHTML:
    def __init__(self, data: str) -> None:
        self.data = data
        self.parser = "lxml"
        self.soup = BeautifulSoup(data, self.parser)

    def remove_image_tags(self) -> None:
        for img in self.soup.find_all("img"):
            img.decompose()
    
    def remove_unordered_list(self) -> None:
        for unordered_list in self.soup.find_all("ul"):
            for li_tags in unordered_list.find_all('li'): # type: ignore
                li_tags.insert_before("\n- ")
            unordered_list.unwrap() # type: ignore
    
    def remove_ordered_list(self) -> None:
        count = 1
        for ordered_list in self.soup.find_all("ol"):
            for li_tags in ordered_list.find_all("li"): # type: ignore
                li_tags.insert_before(f"\n{count}.")
                count += 1
            ordered_list.unwrap() # type: ignore
    
    def remove_other_html_tags(self) -> str:
        return self.soup.get_text(separator="\n")
    
    def decode_html_entities(self) -> str:
        data = self.remove_other_html_tags()
        return html.unescape(s=data)
    
    def normalize_and_break_lines(self) -> str:
        data = self.decode_html_entities()
        normalizing = re.sub(r"[ \t]+", " ", data)
        preserve_line_breaks = re.sub(r"\n\s*\n", "\n\n", normalizing)
        return preserve_line_breaks.strip()
    
    def filtered_result(self) -> str:
        text = self.normalize_and_break_lines()
        return str(text)

        
                


        

        
