import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import json
from pprint import pprint


headers_generator = Headers(os="win", browser="firefox")
response = requests.get(
   "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_generator.generate())
main_html_data = response.text
main_soup = BeautifulSoup(main_html_data, "lxml")

vacancy_list = main_soup.find("main", class_="vacancy-serp-content")
vacancys = vacancy_list.find_all("div", class_='vacancy-serp-item__layout')


vacancys_data = []
for vacancy_tag in vacancys:

   vacancy_link_tag = vacancy_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
   link_relative = vacancy_link_tag["href"]
   link_absolute = f"https://spb.hh.ru{link_relative}"

   city_tag = list(vacancy_tag.find("div", class_="vacancy-serp-item__info"))
   city = city_tag[1].text.strip()

   name_of_company_tag = vacancy_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
   name_of_company = name_of_company_tag.text.strip().replace('\xa0', ' ')

   if vacancy_tag.find("span", class_="bloko-header-section-2"):
      salary_fork = vacancy_tag.find("span", class_="bloko-header-section-2").get_text().replace('\u202f','')

   name_of_vacancy_tag = vacancy_tag.find("a", class_="serp-item__title")
   name_of_vacancy = name_of_vacancy_tag.text.strip()
   pattern = r"Django|Flask|Python"
   result = re.findall(pattern, name_of_vacancy)
   if len(result) > 0:
      vacancys_data.append(
      {
         "name_of_company": name_of_company,
         "ссылка": link_absolute,
         "название города": city,
         "зарплатная вилка": salary_fork,
         "название вакансии": name_of_vacancy

      }
      )
pprint(vacancys_data)

with open("vacancy_data_file.json", "w", encoding="utf-8") as f:
   json.dump(vacancys_data, f, ensure_ascii=False, indent=2)