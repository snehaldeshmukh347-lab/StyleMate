function generateLooks(){

let gender = document.getElementById("gender").value;
let age = document.getElementById("age").value;
let body = document.getElementById("body").value;
let skin = document.getElementById("skin").value;
let occasion = document.getElementById("occasion").value;

if(!gender || !age || !body || !skin || !occasion){
document.getElementById("resultText").innerText = "⚠ Please select all options";
return;
}

document.getElementById("resultText").innerText = "Curated Looks ✨";

let results = document.getElementById("results");
results.innerHTML = "";

/* BRAND + LINKS */
let data = {
Amazon:{
top:"https://www.amazon.in/s?k=women+tops",
pants:"https://www.amazon.in/s?k=women+jeans",
shoes:"https://www.amazon.in/s?k=women+shoes",
acc:"https://www.amazon.in/s?k=women+accessories"
},
Myntra:{
top:"https://www.myntra.com/women-tops",
pants:"https://www.myntra.com/women-jeans",
shoes:"https://www.myntra.com/women-shoes",
acc:"https://www.myntra.com/accessories"
},
"H&M":{
top:"https://www2.hm.com/en_in/women/products/tops.html",
pants:"https://www2.hm.com/en_in/women/products/trousers.html",
shoes:"https://www2.hm.com/en_in/women/products/shoes.html",
acc:"https://www2.hm.com/en_in/women/products/accessories.html"
},
Zara:{
top:"https://www.zara.com/in/en/woman-tops-l1362.html",
pants:"https://www.zara.com/in/en/woman-trousers-l1355.html",
shoes:"https://www.zara.com/in/en/woman-shoes-l1251.html",
acc:"https://www.zara.com/in/en/woman-accessories-l1005.html"
},
Meesho:{
top:"https://www.meesho.com/women-tops/pl/3xf",
pants:"https://www.meesho.com/women-jeans/pl/3nw",
shoes:"https://www.meesho.com/women-footwear/pl/3od",
acc:"https://www.meesho.com/jewellery/pl/3ks"
}
};

/* LOOP */
for(let brand in data){

let card = document.createElement("div");
card.className = "card";

card.innerHTML = `
<h3>${brand}</h3>

<button onclick="window.open('${data[brand].top}')">Top</button>
<button onclick="window.open('${data[brand].pants}')">Pants</button>
<button onclick="window.open('${data[brand].shoes}')">Shoes</button>
<button onclick="window.open('${data[brand].acc}')">Accessories</button>
`;

results.appendChild(card);

}

}