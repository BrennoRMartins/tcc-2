let emoEscolhida = ''; 

function changeButtonColor(color, text, emotion) {
    var pronto = document.getElementById("pronto");
    pronto.style.backgroundColor = color;
    pronto.innerText = text;
    pronto.style.color = "white";
    
    emoEscolhida = emotion; // define a emoção selecionada
};

function analise(emotion){
    alert("Emoção Escolhida " + emotion);
};

// Adiciona evento de clique para cada emoção
document.getElementById("alegria").addEventListener("click", function() {
    changeButtonColor("#f0e002", "Pronto🥳", "alegria");
});
document.getElementById("medo").addEventListener("click", function() {
    changeButtonColor("#9000ce", "Pronto😨", "medo");
});
document.getElementById("nojo").addEventListener("click", function() {
    changeButtonColor("#00ce33", "Pronto😖", "nojo");
});
document.getElementById("raiva").addEventListener("click", function() {
    changeButtonColor("#db0030", "Pronto😠", "raiva");
});
document.getElementById("surpresa").addEventListener("click", function() {
    changeButtonColor("#e00069", "Pronto😲", "surpresa");
});
document.getElementById("tristeza").addEventListener("click", function() {
    changeButtonColor("#007fe0", "Pronto☹️", "tristeza");
});
document.getElementById("amor").addEventListener("click", function() {
    changeButtonColor("#d624b9", "Pronto🥰", "amor");
});
document.getElementById("curiosidade").addEventListener("click", function() {
    changeButtonColor("#193db3", "Pronto🤯", "curiosidade");
});


document.getElementById("pronto").addEventListener("click", function(){
    if (emoEscolhida) {
        window.location.href = `ranking.html?emotion=${encodeURIComponent(emoEscolhida)}`;
    } else {
        alert("Por favor, selecione uma emoção antes de continuar.");
    }
});

document.getElementById("avaliar").addEventListener("click", function(){
    window.location.href = `/formulario`;
});

