const loader = document.getElementById("loader");

// Function to show loader
function showLoader() {
  loader.style.display = "block";
}

// Function to hide loader
function hideLoader() {
  loader.style.display = "none";
}
document.addEventListener("DOMContentLoaded", function () {
  function displayGrievances() {
    const grievanceList = document.getElementById("grievanceList");
    grievanceList.innerHTML = "";

    fetch("http://127.0.0.1:5000/api/grievances/")
      .then((response) => response.json())
      .then((grievances) => {
        grievances.forEach((grievance) => {
          // Create and append the description span
          const li = document.createElement("li");

          const detailsDiv = document.createElement("div");
          detailsDiv.className = "grievance-details";

          const descriptionSpan = document.createElement("span");
          descriptionSpan.className = "description";
          descriptionSpan.textContent = grievance.description;

          const categorySpan = document.createElement("span");
          categorySpan.textContent = `Category: ${grievance.category}`;

          const statusSpan = document.createElement("span");
          statusSpan.textContent = `Status: ${grievance.status}`;
          const assignmentsSpan = document.createElement("span");
          assignmentsSpan.innerHTML =
            "Assigned to: " +
            grievance?.assignments?.map((a) => a.gro_name).join(", ");

          detailsDiv.appendChild(descriptionSpan);
          detailsDiv.appendChild(categorySpan);
          detailsDiv.appendChild(statusSpan);
          detailsDiv.appendChild(assignmentsSpan);

          const actionsDiv = document.createElement("div");
          actionsDiv.className = "grievance-actions";

          const listenButton = document.createElement("button");
          listenButton.innerHTML = "🔊 Listen";
          listenButton.onclick = function () {
            textToSpeech(grievance.description);
          };
          const linksWrapper = document.createElement('div');
          linksWrapper.className = 'links-wrapper'
          const translateLink = document.createElement("a");
          translateLink.href = "#";
          translateLink.innerHTML = "Translate";
          translateLink.onclick = function (event) {
            event.preventDefault();
            // translateText(grievance.description, descriptionSpan, "hi", translateLink); // Example: translate to Hindi
            showLanguageSelection(descriptionSpan, translateLink, 'translate', grievance.description);
          };

          const solutionLink = document.createElement("a");
          solutionLink.href = "#";
          solutionLink.className = "solution";
          solutionLink.innerHTML = "AI Solution";
          solutionLink.onclick = function (event) {
            event.preventDefault(); // Prevent page movement
            // getAISolution(grievance.description, grievance.category);
            showLanguageSelection(descriptionSpan, solutionLink, 'solution', grievance.description, grievance.category);
          };

          linksWrapper.appendChild(translateLink);
          linksWrapper.appendChild(solutionLink);

          actionsDiv.appendChild(listenButton);
          actionsDiv.appendChild(linksWrapper);

          li.appendChild(detailsDiv);
          li.appendChild(actionsDiv);
          grievanceList.appendChild(li);
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error fetching grievances");
      });
  }

  document
    .getElementById("grievanceForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData();
      formData.append(
        "description",
        document.getElementById("description").value
      );
      formData.append("category", document.getElementById("category").value);
      formData.append("userId", document.getElementById("userId").value);

      const image = document.getElementById("image").files[0];
      if (image) {
        formData.append("image", image);
      }
      // Show loader before making the request
      showLoader();
      fetch("http://127.0.0.1:5000/api/grievances/", {
        method: "POST",
        body: formData,
        // headers: {
        //   "Content-Type": "multipart/form-data",
        // },
      })
        .then((response) => response.json())
        .then((data) => {
          // Hide loader after receiving the response
          hideLoader();
          //displayGrievances();
          //   if (data.ai_response) {
          //     alert("AI Response: " + data.ai_response);
          //   }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Error filing grievance");
        });

      document.getElementById("grievanceForm").reset();
    });

  displayGrievances();
});

// Translate Text
function translateText(text, descriptionSpan, targetLang, translateLink) {
  fetch(
    `https://api.mymemory.translated.net/get?q=${encodeURIComponent(
      text
    )}&langpair=en|${targetLang}`
  )
    .then((response) => response.json())
    .then((data) => {
      if (data.responseData.translatedText) {
        const originalText = text;
        const translatedText = data.responseData.translatedText;

        descriptionSpan.innerHTML = translatedText;

        const originalLink = document.createElement("a");
        originalLink.href = "#";
        originalLink.innerHTML = "Original";
        originalLink.className = 'original';
        originalLink.onclick = function (event) {
          event.preventDefault(); // Prevent page movement
          descriptionSpan.innerHTML = originalText;
          originalLink.style.display = 'none'; // Hide original link
          translateLink.style.display = "inline"; // Show translate link
          //originalLink.remove(); // Remove original link
        };

        translateLink.style.display = "none"; // Hide translate link
        translateLink.parentElement.appendChild(originalLink);
      } else {
        alert("Translation failed.");
      }
    })
    .catch((error) => {
      // console.error("Error:", error);
      alert("Error with translation.");
    });
}

// Get AI Solution
// Get AI Solution
function getAISolution(description, category, targetLang) {
  const formData = new FormData();
  formData.append("description", description);
  formData.append("category", category);
  formData.append('language', targetLang);
  // Show loader before making the request
  showLoader();
  fetch("http://127.0.0.1:5000/api/grievances/solution", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Hide loader after receiving the response
      hideLoader();
      if (data.solution) {
        showSolutionModal(data.solution);
      } else {
        alert("No solution found.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error fetching AI solution.");
    });
}

// Show Solution Modal
function showSolutionModal(solution) {
  const modal = document.getElementById("solutionModal");
  const solutionText = document.getElementById("solutionText");
  const closeButton = document.getElementsByClassName("close")[0];

  solutionText.textContent = solution;
  modal.style.display = "block";

  closeButton.onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
}

// Initialize Speech Recognition
const startRecordBtn = document.getElementById("start-record-btn");
const descriptionInput = document.getElementById("description");
const recognition = new (window.SpeechRecognition ||
  window.webkitSpeechRecognition)();
recognition.lang = "en-IN"; // Set language to Hindi or English as needed

startRecordBtn.addEventListener("click", () => {
  recognition.start();
});

recognition.onresult = function (event) {
  const transcript = event.results[0][0].transcript;
  descriptionInput.value = transcript;
};

recognition.onerror = function (event) {
  console.error("Speech recognition error:", event.error);
  alert("Error with speech recognition: " + event.error);
};

// Text to Speech
function textToSpeech(text) {
  const speech = new SpeechSynthesisUtterance();
  speech.lang = "en-IN"; // Set language to Hindi or English as needed
  speech.text = text;
  speech.volume = 1;
  speech.rate = 1;
  speech.pitch = 1;

  window.speechSynthesis.speak(speech);
}
// Show language selection and perform action (translate or solution)
function showLanguageSelection(descriptionSpan, actionLink, actionType, description, category = null) {
  const languageDropdown = document.createElement('select');
  const languages = [
      { value: 'en', text: 'English' },
      { value: 'hi', text: 'Hindi' },
      { value: 'ta', text: 'Tamil' },
      { value: 'bn', text: 'Bengali' },
      { value: 'zh', text: 'Chinese' }
  ];

  languages.forEach(lang => {
      const option = document.createElement('option');
      option.value = lang.value;
      option.text = lang.text;
      languageDropdown.appendChild(option);
  });

  actionLink.style.display = 'none';
  actionLink.parentElement.appendChild(languageDropdown);

  const confirmButton = document.createElement('button');
  confirmButton.innerHTML = 'Confirm';
  confirmButton.onclick = function() {
      const selectedLanguage = languageDropdown.value;
      if (actionType === 'translate') {
          translateText(description, descriptionSpan, selectedLanguage, actionLink);
      } else if (actionType === 'solution') {
          getAISolution(description, category, selectedLanguage);
      }

      languageDropdown.remove();
      confirmButton.remove();
  };

  actionLink.parentElement.appendChild(confirmButton);
}
