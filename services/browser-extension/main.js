let myDeals = JSON.parse(localStorage.getItem("myDeals")) || [];
let currentCarIndex = Number(localStorage.getItem("currentCarIndex")) || 0;
findDeal = document.getElementById("find-deal");
navigateDeals = document.getElementById("navigate-deals");
nextButton = document.getElementById("next");
prevButton = document.getElementById("prev");
currentPage = document.getElementById("current-page");
totalPages = document.getElementById("total-pages");
spinner = document.getElementById("spinner");
refresh = document.getElementById("refresh");
error = document.getElementById("error");

const setDisabled = () => {
  if (currentCarIndex >= myDeals.length - 1) {
    nextButton.disabled = true;
  } else {
    nextButton.disabled = false;
  }
  if (currentCarIndex <= 0) {
    prevButton.disabled = true;
  } else {
    prevButton.disabled = false;
  }
};

const init = () => {
  if (myDeals.length > 0) {
    navigateDeals.classList.remove("hidden");
    navigateDeals.classList.add("block");
    refresh.classList.add("block");
    refresh.classList.remove("hidden");
    setDisabled();
  } else {
    navigateDeals.classList.add("hidden");
    navigateDeals.classList.remove("block");
    refresh.classList.remove("block");
    refresh.classList.add("hidden");
  }
  currentPage.innerText = currentCarIndex + 1;
  totalPages.innerText = myDeals.length;
};

const triggerRefresh = () => {
  myDeals = [];
  currentCarIndex = 0;
  localStorage.setItem("myDeals", JSON.stringify(myDeals));
  localStorage.setItem("currentCarIndex", currentCarIndex);
  init();
};

refresh.addEventListener("click", triggerRefresh);

findDeal.addEventListener("click", async (e) => {
  triggerRefresh();

  chrome.tabs.query({ active: true, lastFocusedWindow: true }, async (tabs) => {
    let url = tabs[0].url;

    spinner.classList.remove("hidden");
    spinner.classList.add("block");

    try {
      const res = await fetch(`http://127.0.0.1:5000/?request_url=${url}`);
      data = await res.json();
      myDeals = data;
    } catch (err) {
      error.classList.remove("hidden");
      error.classList.add("block");
      triggerRefresh();
    }

    localStorage.setItem("myDeals", JSON.stringify(myDeals));

    spinner.classList.add("hidden");
    spinner.classList.remove("block");

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      chrome.tabs.update(tabs[0].id, {
        url: myDeals[currentCarIndex],
      });
    });
  });
});

nextButton.addEventListener("click", (e) => {
  currentCarIndex++;
  localStorage.setItem("currentCarIndex", currentCarIndex);

  setDisabled();

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.update(tabs[0].id, {
      url: myDeals[currentCarIndex],
    });
  });
  currentPage.innerText = currentCarIndex + 1;
});

prevButton.addEventListener("click", (e) => {
  currentCarIndex--;
  localStorage.setItem("currentCarIndex", currentCarIndex);

  setDisabled();

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.update(tabs[0].id, {
      url: myDeals[currentCarIndex],
    });
  });
  currentPage.innerText = currentCarIndex + 1;
});

init();
