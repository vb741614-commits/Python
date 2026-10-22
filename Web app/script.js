const dialog = document.querySelector("#love-dialog");
const photoDialog = document.querySelector("#photo-dialog");
const surpriseDialog = document.querySelector("#surprise-dialog");
const photoImage = document.querySelector("#photo-viewer-img");
const photoNoteTitle = document.querySelector("#photo-note-title");
const photoNoteMessage = document.querySelector("#photo-note-message");
const photoCounter = document.querySelector("#photo-counter");
const toast = document.querySelector("#toast");
const confettiLayer = document.querySelector("#confetti-layer");
let toastTimer;
let activePhotoIndex = 0;

const photos = [
  {
    file: "darling-1.jpg",
    title: "You, stealing the whole view",
    note: "That view is beautiful, but somehow you’re still the first thing I notice. I’d go anywhere just to share a moment like this with you, Darling.",
  },
  {
    file: "darling-2.jpg",
    title: "My sunshine in yellow",
    note: "You look lovely in every color, but this one feels like it was made to match the light you bring into my life. I could look at you all day, Darling.",
  },
  {
    file: "darling-3.jpg",
    title: "My favorite view: us",
    note: "This is my favorite kind of picture: the two of us together. Every little adventure is better when I get to be right beside you.",
  },
];

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("is-visible");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("is-visible"), 3200);
}

function celebrate(count = 14, symbols = ["♥", "♡"]) {
  const colors = ["#c85f65", "#e7a28d", "#d5a85f", "#f0c6ad", "#a7af7c"];

  for (let index = 0; index < count; index += 1) {
    const heart = document.createElement("span");
    heart.className = "confetti-heart";
    heart.textContent = symbols[Math.floor(Math.random() * symbols.length)];
    heart.style.left = `${Math.random() * 100}%`;
    heart.style.color = colors[Math.floor(Math.random() * colors.length)];
    heart.style.fontSize = `${14 + Math.random() * 17}px`;
    heart.style.animationDelay = `${Math.random() * 0.45}s`;
    confettiLayer.append(heart);
    heart.addEventListener("animationend", () => heart.remove(), { once: true });
  }
}

function updatePhoto(index) {
  activePhotoIndex = (index + photos.length) % photos.length;
  const photo = photos[activePhotoIndex];

  if (photoImage.dataset.photoFile !== photo.file) {
    photoImage.parentElement.classList.remove("has-photo");
    photoImage.dataset.loaded = "false";
    photoImage.src = `/photos/${photo.file}`;
    photoImage.dataset.photoFile = photo.file;
  } else if (photoImage.dataset.loaded === "true") {
    photoImage.parentElement.classList.add("has-photo");
  }
  photoImage.alt = photo.title;
  photoNoteTitle.textContent = photo.title;
  photoNoteMessage.textContent = photo.note;
  photoCounter.textContent = `${String(activePhotoIndex + 1).padStart(2, "0")} / ${String(photos.length).padStart(2, "0")}`;
  document.querySelectorAll(".gallery-card").forEach((card) => {
    const image = card.querySelector("img");
    const isActive = card.dataset.photo === photo.file;
    if (isActive) card.setAttribute("aria-current", "true");
    else card.removeAttribute("aria-current");
    if (isActive && image.dataset.loaded === "true") {
      photoImage.parentElement.classList.add("has-photo");
    }
  });
}

document.querySelectorAll(".gallery-card img, #photo-viewer-img").forEach((image) => {
  image.addEventListener("load", () => {
    image.dataset.loaded = "true";
    image.parentElement.classList.add("has-photo");
  });
  image.addEventListener("error", () => {
    image.dataset.loaded = "false";
    image.parentElement.classList.remove("has-photo");
  });
});

document.querySelectorAll(".gallery-card").forEach((card, index) => {
  card.addEventListener("click", () => {
    updatePhoto(index);
    photoDialog.showModal();
    celebrate(12, ["♥", "♡", "✿", "💋", "🌸"]);
  });
});

document.querySelector("#surprise-button").addEventListener("click", () => {
  document.querySelectorAll(".surprise-photo").forEach((card, index) => {
    card.setAttribute("aria-pressed", "false");
    card.setAttribute("aria-label", `Flip to reveal ${photos[index].title}`);
    card.querySelector(".surprise-photo-front").setAttribute("aria-hidden", "false");
    card.querySelector(".surprise-photo-back").setAttribute("aria-hidden", "true");
  });
  surpriseDialog.showModal();
  celebrate(18, ["♥", "♡", "✿", "💋", "🌸"]);
});

document.querySelectorAll(".surprise-photo").forEach((card, index) => {
  card.addEventListener("click", () => {
    const isFlipped = card.getAttribute("aria-pressed") !== "true";
    card.setAttribute("aria-pressed", String(isFlipped));
    card.setAttribute(
      "aria-label",
      `${isFlipped ? "Flip to hide" : "Flip to reveal"} ${photos[index].title}`,
    );
    card.querySelector(".surprise-photo-front").setAttribute("aria-hidden", String(isFlipped));
    card.querySelector(".surprise-photo-back").setAttribute("aria-hidden", String(!isFlipped));
    if (isFlipped) celebrate(5, ["♥", "♡", "✿"]);
  });
});

document.querySelector(".photo-prev").addEventListener("click", () => updatePhoto(activePhotoIndex - 1));
document.querySelector(".photo-next").addEventListener("click", () => updatePhoto(activePhotoIndex + 1));

document.querySelector("#letter-button").addEventListener("click", () => {
  dialog.showModal();
  celebrate(10);
});

document.querySelector("#heart-button").addEventListener("click", () => {
  celebrate(22);
  showToast("A little reminder: you are someone's favorite person. ♡");
});

document.querySelectorAll(".reason-card").forEach((card) => {
  card.addEventListener("click", () => showToast(card.dataset.reason));
});

document.querySelector("#hug-button").addEventListener("click", () => {
  celebrate(18);
  showToast("Sending you the biggest, coziest hug. Hold it as long as you need. ♡");
});

dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

photoDialog.addEventListener("click", (event) => {
  if (event.target === photoDialog) photoDialog.close();
});

surpriseDialog.addEventListener("click", (event) => {
  if (event.target === surpriseDialog) surpriseDialog.close();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && dialog.open) dialog.close();
  if (event.key === "Escape" && photoDialog.open) photoDialog.close();
  if (event.key === "Escape" && surpriseDialog.open) surpriseDialog.close();
  if (event.key === "ArrowLeft" && photoDialog.open) updatePhoto(activePhotoIndex - 1);
  if (event.key === "ArrowRight" && photoDialog.open) updatePhoto(activePhotoIndex + 1);
});
