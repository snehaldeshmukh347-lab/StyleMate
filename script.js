// ============================================================
// STYLEMATE STATE & USER PROFILE
// ============================================================

const userData = {
    audience: "Women",
    kidsAge: "Toddler (2–4 yrs)",
    bodyType: "Hourglass",
    skinTone: "Medium",
    colors: ["Black", "Beige"],
    occasion: "Beach",
    style: "Western",
    photo: ""
};

let currentLooks = [];
let activeLookIndex = 0;

// Dynamic Form Configuration based on User Type and Kids Age Group
const OCCASIONS_BY_CONFIG = {
    Women: [
        { label: "Beach Party", value: "Beach" },
        { label: "Office & Corporate", value: "Office" },
        { label: "Casual Weekend", value: "Casual" },
        { label: "College & Campus", value: "College" },
        { label: "Night Club / Party", value: "Party" },
        { label: "Romantic Date", value: "Date" },
        { label: "Wedding & Gala", value: "Wedding" },
        { label: "Reception", value: "Reception" },
        { label: "Festive / Diwali", value: "Festive" },
        { label: "Traditional", value: "Traditional" },
        { label: "Vacation & Resort", value: "Vacation" },
        { label: "Travel", value: "Travel" },
        { label: "Dinner", value: "Dinner" },
        { label: "Sunday Brunch", value: "Brunch" },
        { label: "Concert / Fest", value: "Concert" },
        { label: "Interview", value: "Interview" },
        { label: "Family Function", value: "Family Function" },
        { label: "Sports & Athleisure", value: "Sports" }
    ],
    Men: [
        { label: "Office & Corporate", value: "Office" },
        { label: "Casual Weekend", value: "Casual" },
        { label: "College & Campus", value: "College" },
        { label: "Party & Club", value: "Party" },
        { label: "Wedding & Formal", value: "Wedding" },
        { label: "Festive / Diwali", value: "Festive" },
        { label: "Vacation & Resort", value: "Vacation" },
        { label: "Travel", value: "Travel" },
        { label: "Dinner Date", value: "Date" },
        { label: "Interview", value: "Interview" },
        { label: "Sports & Athleisure", value: "Sports" }
    ],
    Kids: {
        "Toddler (2–4 yrs)": [
            { label: "Everyday", value: "Everyday" },
            { label: "Party", value: "Party" },
            { label: "Birthday", value: "Birthday" },
            { label: "Wedding / Family Function", value: "Wedding / Family Function" },
            { label: "Festive / Diwali", value: "Festive / Diwali" },
            { label: "Vacation", value: "Vacation" },
            { label: "Play / Outdoor", value: "Play / Outdoor" }
        ],
        "Little Kids (5–8 yrs)": [
            { label: "Everyday", value: "Everyday" },
            { label: "School / Study", value: "School / Study" },
            { label: "Party", value: "Party" },
            { label: "Birthday", value: "Birthday" },
            { label: "Wedding / Family Function", value: "Wedding / Family Function" },
            { label: "Festive / Diwali", value: "Festive / Diwali" },
            { label: "Vacation", value: "Vacation" },
            { label: "Play / Outdoor", value: "Play / Outdoor" }
        ],
        "Pre-Teen (9–12 yrs)": [
            { label: "Everyday", value: "Everyday" },
            { label: "School / Study", value: "School / Study" },
            { label: "Party", value: "Party" },
            { label: "Birthday", value: "Birthday" },
            { label: "Wedding / Family Function", value: "Wedding / Family Function" },
            { label: "Festive / Diwali", value: "Festive / Diwali" },
            { label: "Vacation", value: "Vacation" },
            { label: "Sports / Outdoor", value: "Sports / Outdoor" }
        ],
        "Teen (13–16 yrs)": [
            { label: "Casual", value: "Casual" },
            { label: "Campus", value: "Campus" },
            { label: "Party", value: "Party" },
            { label: "Wedding / Family Function", value: "Wedding / Family Function" },
            { label: "Festive / Diwali", value: "Festive / Diwali" },
            { label: "Vacation", value: "Vacation" },
            { label: "Sports / Athleisure", value: "Sports / Athleisure" },
            { label: "Special Occasion", value: "Special Occasion" }
        ]
    }
};

const AESTHETICS_BY_CONFIG = {
    Women: [
        { label: "Western Chic", value: "Western" },
        { label: "Traditional Indian", value: "Indian" },
        { label: "Indo-Western Fusion", value: "Fusion" },
        { label: "Clean Minimal", value: "Minimal" },
        { label: "Streetwear", value: "Streetwear" },
        { label: "Old Money Luxe", value: "Elegant" },
        { label: "Sporty Athleisure", value: "Sporty" },
        { label: "Boho Chic", value: "Boho" },
        { label: "Runway Trendy", value: "Trendy" },
        { label: "Y2K Nostalgia", value: "Y2K" }
    ],
    Men: [
        { label: "Western Chic", value: "Western" },
        { label: "Traditional Indian", value: "Indian" },
        { label: "Indo-Western Fusion", value: "Fusion" },
        { label: "Clean Minimal", value: "Minimal" },
        { label: "Streetwear", value: "Streetwear" },
        { label: "Old Money Luxe", value: "Elegant" },
        { label: "Sporty Athleisure", value: "Sporty" }
    ],
    Kids: {
        Young: [
            { label: "Cute & Playful", value: "Cute & Playful" },
            { label: "Simple & Comfortable", value: "Simple & Comfortable" },
            { label: "Trendy", value: "Trendy" },
            { label: "Pretty & Elegant", value: "Pretty & Elegant" },
            { label: "Cozy", value: "Cozy" },
            { label: "Sporty", value: "Sporty" },
            { label: "Fun & Colourful", value: "Fun & Colourful" },
            { label: "Minimal", value: "Minimal" }
        ],
        Teen: [
            { label: "Clean Minimal", value: "Clean Minimal" },
            { label: "Streetwear", value: "Streetwear" },
            { label: "Trendy", value: "Trendy" },
            { label: "Sporty", value: "Sporty" },
            { label: "Y2K", value: "Y2K" },
            { label: "Soft Girl", value: "Soft Girl" },
            { label: "Casual Chic", value: "Casual Chic" },
            { label: "Indo-Western", value: "Indo-Western" }
        ]
    }
};

// URL Query Params Check (e.g. app.html?path=chat or ?path=wizard&occasion=Office)
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const pathParam = params.get("path");
    const occasionParam = params.get("occasion");

    if (occasionParam) {
        userData.occasion = occasionParam;
    }

    if (pathParam === "chat") {
        switchPath("chat");
    } else {
        switchPath("wizard");
    }

    updateDynamicFormOptions();
});

// ============================================================
// PATH SWITCHER LOGIC
// ============================================================

const path1Btn = document.getElementById("path1Btn");
const path2Btn = document.getElementById("path2Btn");
const path1Container = document.getElementById("path1Container");
const chatSection = document.getElementById("chat");
const pathHeading = document.getElementById("pathHeading");
const pathSubheading = document.getElementById("pathSubheading");

if (path1Btn && path2Btn) {
    path1Btn.addEventListener("click", () => switchPath("wizard"));
    path2Btn.addEventListener("click", () => switchPath("chat"));
}

function switchPath(mode) {
    if (!path1Container || !chatSection) return;

    if (mode === "chat") {
        path1Btn.classList.remove("active");
        path2Btn.classList.add("active");
        path1Container.style.display = "none";
        pathHeading.innerHTML = "Ask your <em>stylist.</em>";
        pathSubheading.innerHTML = "Describe what you want naturally or instruct StyleMate to generate a custom look directly.";
        chatSection.scrollIntoView({ behavior: "smooth" });
    } else {
        path2Btn.classList.remove("active");
        path1Btn.classList.add("active");
        path1Container.style.display = "block";
        pathHeading.innerHTML = "Create a look<br><em>made for you.</em>";
        pathSubheading.innerHTML = "Tell us who you are, what you're dressing for, and your vibe. StyleMate AI will decide the complete outfit.";
    }
}

// ============================================================
// DYNAMIC FORM RENDERING LOGIC
// ============================================================

function updateDynamicFormOptions() {
    const occContainer = document.getElementById("occasionChoices");
    const styleContainer = document.getElementById("styleChoices");
    const bodyField = document.getElementById("bodyTypeField");
    const kidsBox = document.getElementById("kidsAgeGroup");

    if (userData.audience === "Kids") {
        if (kidsBox) kidsBox.classList.remove("hidden");
        if (bodyField) bodyField.style.display = "none";
    } else {
        if (kidsBox) kidsBox.classList.add("hidden");
        if (bodyField) bodyField.style.display = "flex";
    }

    // Get active occasions list
    let availableOccasions = [];
    if (userData.audience === "Kids") {
        availableOccasions = OCCASIONS_BY_CONFIG.Kids[userData.kidsAge] || OCCASIONS_BY_CONFIG.Kids["Toddler (2–4 yrs)"];
    } else {
        availableOccasions = OCCASIONS_BY_CONFIG[userData.audience] || OCCASIONS_BY_CONFIG.Women;
    }

    // Get active aesthetics list
    let availableStyles = [];
    if (userData.audience === "Kids") {
        if (userData.kidsAge && userData.kidsAge.includes("Teen")) {
            availableStyles = AESTHETICS_BY_CONFIG.Kids.Teen;
        } else {
            availableStyles = AESTHETICS_BY_CONFIG.Kids.Young;
        }
    } else {
        availableStyles = AESTHETICS_BY_CONFIG[userData.audience] || AESTHETICS_BY_CONFIG.Women;
    }

    // Ensure valid current selected occasion
    const isValidOccasion = availableOccasions.some(o => o.value.toLowerCase() === userData.occasion.toLowerCase() || o.label.toLowerCase() === userData.occasion.toLowerCase());
    if (!isValidOccasion && availableOccasions.length > 0) {
        userData.occasion = availableOccasions[0].value;
    }

    // Ensure valid current selected style
    const isValidStyle = availableStyles.some(s => s.value.toLowerCase() === userData.style.toLowerCase() || s.label.toLowerCase() === userData.style.toLowerCase());
    if (!isValidStyle && availableStyles.length > 0) {
        userData.style = availableStyles[0].value;
    }

    // Render Occasions Grid
    if (occContainer) {
        occContainer.innerHTML = availableOccasions.map(o => {
            const isSelected = o.value.toLowerCase() === userData.occasion.toLowerCase() || o.label.toLowerCase() === userData.occasion.toLowerCase();
            return `<button class="choice ${isSelected ? 'selected' : ''}" data-value="${o.value}">${o.label}</button>`;
        }).join("");

        occContainer.querySelectorAll(".choice").forEach(btn => {
            btn.addEventListener("click", function() {
                occContainer.querySelectorAll(".choice").forEach(b => b.classList.remove("selected"));
                this.classList.add("selected");
                userData.occasion = this.dataset.value;
            });
        });
    }

    // Render Aesthetics Grid
    if (styleContainer) {
        styleContainer.innerHTML = availableStyles.map(s => {
            const isSelected = s.value.toLowerCase() === userData.style.toLowerCase() || s.label.toLowerCase() === userData.style.toLowerCase();
            return `<button class="choice ${isSelected ? 'selected' : ''}" data-group="style" data-value="${s.value}">${s.label}</button>`;
        }).join("");

        styleContainer.querySelectorAll(".choice").forEach(btn => {
            btn.addEventListener("click", function() {
                styleContainer.querySelectorAll(".choice").forEach(b => b.classList.remove("selected"));
                this.classList.add("selected");
                userData.style = this.dataset.value;
            });
        });
    }
}

// ============================================================
// CHOICE BUTTON HANDLERS
// ============================================================

document.querySelectorAll("#audienceChoices .choice").forEach(button => {
    button.addEventListener("click", function () {
        document.querySelectorAll('#audienceChoices .choice').forEach(b => b.classList.remove("selected"));
        this.classList.add("selected");
        userData.audience = this.dataset.value;
        updateDynamicFormOptions();
    });
});

document.querySelectorAll("#kidsAgeGroup .choice").forEach(button => {
    button.addEventListener("click", function () {
        document.querySelectorAll('#kidsAgeGroup .choice').forEach(b => b.classList.remove("selected"));
        this.classList.add("selected");
        userData.kidsAge = this.dataset.value;
        updateDynamicFormOptions();
    });
});

// ============================================================
// COLOR PILLS MULTI-SELECT
// ============================================================

document.querySelectorAll(".color-pill").forEach(pill => {
    pill.addEventListener("click", function () {
        const color = this.dataset.color;

        if (color === "No Preference") {
            document.querySelectorAll(".color-pill").forEach(p => p.classList.remove("selected"));
            this.classList.add("selected");
            userData.colors = ["No Preference"];
            return;
        }

        document.querySelector('.color-pill[data-color="No Preference"]')?.classList.remove("selected");

        if (this.classList.contains("selected")) {
            this.classList.remove("selected");
            userData.colors = userData.colors.filter(c => c !== color);
        } else {
            this.classList.add("selected");
            if (!userData.colors.includes(color)) {
                userData.colors.push(color);
            }
        }

        if (userData.colors.length === 0) {
            userData.colors = ["No Preference"];
            document.querySelector('.color-pill[data-color="No Preference"]')?.classList.add("selected");
        }
    });
});

// Photo upload listener
const photoInput = document.getElementById("photo");
if (photoInput) {
    photoInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            userData.photo = file.name;
            const labelText = document.getElementById("uploadLabelText");
            if (labelText) labelText.textContent = `✓ Photo uploaded (${file.name})`;
        }
    });
}

// ============================================================
// GENERATE OUTFITS (PATH 1)
// ============================================================

const generateBtn = document.getElementById("generateBtn");
if (generateBtn) {
    generateBtn.addEventListener("click", async () => {
        userData.bodyType = document.getElementById("bodyType")?.value || "Hourglass";
        userData.skinTone = document.getElementById("skinTone")?.value || "Medium";

        const status = document.getElementById("status");
        if (status) status.textContent = "StyleMate AI is crafting your 3 personalized outfits... ✨";

        try {
            const response = await fetch("http://127.0.0.1:5000/api/generate-outfit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData)
            });

            if (!response.ok) throw new Error("Server returned " + response.status);

            const data = await response.json();
            currentLooks = data.looks || [];
            activeLookIndex = 0;

            document.getElementById("resultSection")?.classList.remove("hidden");
            renderActiveLook();

            if (status) status.textContent = "";
            document.getElementById("resultSection")?.scrollIntoView({ behavior: "smooth" });

        } catch (error) {
            console.error("StyleMate error:", error);
            if (status) status.textContent = "Couldn't connect to StyleMate backend. Ensure Flask server is running.";
        }
    });
}

// ============================================================
// RENDER LOOK TABS & ACTIVE LOOK
// ============================================================

function renderActiveLook() {
    if (!currentLooks || currentLooks.length === 0) return;

    const look = currentLooks[activeLookIndex];
    const resultDiv = document.getElementById("result");
    if (!resultDiv) return;

    // Render Tabs
    const tabsContainer = document.getElementById("lookTabsContainer");
    if (tabsContainer) {
        tabsContainer.innerHTML = currentLooks.map((l, idx) => `
            <button class="look-tab ${idx === activeLookIndex ? 'active' : ''}" onclick="switchLookTab(${idx})">
                ${l.name ? l.name.split('·')[0].trim() : `LOOK 0${idx+1}`}
            </button>
        `).join("");
    }

    // Items Render
    const labelMap = {
        "top": "TOP",
        "bottom_or_dress": "BOTTOM / DRESS",
        "shoes": "FOOTWEAR",
        "outerwear": "OUTERWEAR",
        "accessories": "ACCESSORIES",
        "bag": "BAG / HANDBAG",
        "styling": "STYLING & HAIR",
        "main": "MAIN PIECE",
        "bottom": "BOTTOM"
    };

    const itemsHTML = Object.entries(look.items || {}).map(([category, val]) => {
        if (!val || val.toString().toLowerCase() === "none" || val.toString().toLowerCase() === "n/a") return "";
        const labelText = labelMap[category] || category.replace(/_/g, " ").toUpperCase();
        const shopLinks = look.shopping?.[category] || {};
        return `
            <div class="outfit-item-card">
                <span class="item-label-tag">${labelText}</span>
                <div class="item-title">${val}</div>
                <div class="shop-links-bar">
                    ${shopLinks.Amazon ? `<a href="${shopLinks.Amazon}" target="_blank" class="shop-btn">Amazon</a>` : ''}
                    ${shopLinks.Myntra ? `<a href="${shopLinks.Myntra}" target="_blank" class="shop-btn">Myntra</a>` : ''}
                    ${shopLinks.AJIO ? `<a href="${shopLinks.AJIO}" target="_blank" class="shop-btn">AJIO</a>` : ''}
                </div>
            </div>
        `;
    }).join("");

    resultDiv.innerHTML = `
        <div class="look-card-render">
            <h3 class="look-card-title">${look.name || "Curated Look"}</h3>
            <p class="look-card-desc">${look.description || ""}</p>

            <div class="outfit-grid">
                ${itemsHTML}
            </div>

            <div style="margin-top: 25px; border-top: 1px solid #d4cec2; padding-top: 20px;">
                <strong>Palette:</strong> ${look.colors || "Neutrals"}<br>
                <strong>Styling Advice:</strong> ${look.styling_tip || "Soft natural glow finish."}<br><br>
                <strong>Why This Outfit Works:</strong><br>
                <p style="color: #555; margin-top: 5px;">${look.why_it_works || "Complements proportions and skin tone."}</p>
            </div>
        </div>
    `;
}

window.switchLookTab = function(index) {
    activeLookIndex = index;
    renderActiveLook();
};

// ============================================================
// CHATBOT & OUTFIT MODIFICATION
// ============================================================

const chatBtn = document.getElementById("chatBtn");
const chatInput = document.getElementById("chatInput");

if (chatBtn) chatBtn.addEventListener("click", () => sendMessage());
if (chatInput) {
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
}

document.querySelectorAll(".tweak-btn").forEach(btn => {
    btn.addEventListener("click", function() {
        const text = this.getAttribute("data-tweak");
        if (text) sendMessage(text);
    });
});

async function sendMessage(userText = null) {
    const text = userText || chatInput?.value.trim();
    if (!text) return;

    if (chatInput) chatInput.value = "";

    const chatBox = document.getElementById("chatBox");
    if (!chatBox) return;

    chatBox.innerHTML += `<div class="user-message"><strong>You:</strong> ${text}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    const currentOutfit = currentLooks[activeLookIndex] || null;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                profile: userData,
                current_outfit: currentOutfit
            })
        });

        const data = await response.json();

        chatBox.innerHTML += `<div class="bot-message"><strong>StyleMate:</strong> ${data.reply || "I've adjusted your outfit recommendations!"}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        if (data.updated_outfit) {
            if (currentLooks.length > 0) {
                currentLooks[activeLookIndex] = data.updated_outfit;
            } else {
                currentLooks = [data.updated_outfit];
                activeLookIndex = 0;
            }
            document.getElementById("resultSection")?.classList.remove("hidden");
            renderActiveLook();
        }

    } catch (error) {
        console.error("Chat error:", error);
        chatBox.innerHTML += `<div class="bot-message"><strong>StyleMate:</strong> Connection error. Make sure Flask backend is running on port 5000.</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}