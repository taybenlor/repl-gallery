const search = document.getElementById("search") as HTMLInputElement;
search.addEventListener("input", () => {
  const term = search.value.trim().toLowerCase();
  for (const el of document.querySelectorAll(
    "[data-search]"
  ) as NodeListOf<HTMLElement>) {
    const elSearch = el.getAttribute("data-search").toLowerCase();
    if (elSearch.includes(term)) {
      el.style.display = null;
    } else {
      el.style.display = "none";
    }
  }
});

const random = document.getElementById("random") as HTMLButtonElement;
random.addEventListener("click", () => {
  const elements = document.querySelectorAll(
    "[data-search]"
  ) as NodeListOf<HTMLElement>;
  const index = Math.floor(Math.random() * elements.length);
  const element = elements.item(index);
  window.location.href = element.getAttribute("href");
});
