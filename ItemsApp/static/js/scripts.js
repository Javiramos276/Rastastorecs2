document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los formularios en la página
    const forms = document.querySelectorAll('form');
    
    // Adjuntar evento submit a cada formulario
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Obtener la posición actual de desplazamiento
            const scrollPos = window.scrollY;
            sessionStorage.setItem('scrollPos', scrollPos);
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Desactivar la animación de desplazamiento suave para el restablecimiento instantáneo
    document.documentElement.style.scrollBehavior = 'auto';

    // Obtener la posición almacenada de desplazamiento
    const scrollPos = sessionStorage.getItem('scrollPos');
    
    // Restaurar la posición de desplazamiento si está almacenada
    if (scrollPos) {
        window.scrollTo(0, parseInt(scrollPos));
        sessionStorage.removeItem('scrollPos');
    }

    // Reactivar la animación de desplazamiento suave después del restablecimiento
    document.documentElement.style.scrollBehavior = '';

});


const rangeInput = document.querySelectorAll(".range-input input");
priceInput = document.querySelectorAll(".price-input input")
progress = document.querySelector(".slider-price .progress-price");


let priceGap = 1000;

priceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        //Obtenemos los rangos de valores
        let minVal = parseInt(priceInput[0].value),
        maxVal = parseInt(priceInput[1].value);

        if((maxVal - minVal >= priceGap) && maxVal <= 100000){
            if(e.target.classname === "input-min"){
                rangeInput[0].value = minVal;
                progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            }else{
                rangeInput[1].value = minVal + priceGap;
                progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
            }
        }

        
    });
})


rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        //Obtenemos los rangos de valores
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        if(maxVal - minVal < priceGap){
            if(e.target.classname === "range-min"){
                rangeInput[0].value = maxVal - priceGap;
            }else{
                rangeInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }

        console.log(minVal)
        console.log(maxVal)
    })
})

// const listarArmasPrecios = async () =>{
//     const rangeMin = document.querySelector('.range-min');
//     const rangeMax = document.querySelector('.range-max');
//     const minVal = parseInt(rangeMin.value);
//     const maxVal = parseInt(rangeMax.value);

//     if (maxVal-minVal <= priceGap){
//         try {
//             const response= await fetch(`/get_precios/?minVal=${minVal}&maxVal=${maxVal}`);
//             const data = await response.json();
//             console.log(data)
            
//         } catch (error) {
//             console.log(error);
//         }
//     }
// }

// const cargaInicial = async () =>{
//     await listarArmasPrecios();
// }

// window.addEventListener("load", async () =>{
//     await cargaInicial();
// })

//JUAN cuando se carga completamente el DOM
document.addEventListener('DOMContentLoaded', () => {
    //JUAN Hacer un fetch unica vez para obtener todas las armas (Que en realidad es un JSON enorme)

    const obtenerPrecios = async () => {
        const response = await fetch(`./get_precios`);
        const data = await response.json();
    }
    //contruir la vista de todas las armas (iterar el super JSON y mostrar cada elemento en el DOM)

    //averiguar como obtener el evento o detectar que el slide se movio para ejecutar la funcion "filter items"

    const rangeMin = document.querySelector('.range-min'); // Seleccionamos los rangos maximos y minimos
    const rangeMax = document.querySelector('.range-max');
    const priceGap = 200;

    const rangeInput = [rangeMin, rangeMax];
    const armaContainer = document.querySelector('.d-flex.flex-wrap.justify-content-around.px-5.w-75.m-l-3');
    
    const updatePrices = async () => {
        const minVal = parseInt(rangeMin.value); // Obtenemos el valor mínimo y máximo
        const maxVal = parseInt(rangeMax.value);
        
        
        if (data.message === "Success") {
            if (maxVal - minVal >= priceGap) {
                console.log(data);

                // Insertar nuevos resultados
                data.armas.forEach(arma => {
                    const imgArma = document.getElementById(`img-arma-${arma.id}`); // Obtenemos el id del elemento que contiene la imagen del arma
                    const armaFullName = document.getElementById(`full-name-arma-${arma.id}`);
                    const armaName = document.getElementById(`item-name-arma-${arma.id}`);
                    const qualityArma = document.getElementById(`quality-arma-${arma.id}`);
                    const floatArma = document.getElementById(`floatArma-${arma.id}`);
                    const ArmaPrecio = document.getElementById(`ArmaPrecio-${arma.id}`);

                    imgArma.src = arma.imageurl;
                    armaFullName.innerText = arma.full_item_name;
                    armaName.innerText = arma.item_name;
                    qualityArma.innerText = arma.quality_name;
                    floatArma.innerText = arma.floatvalue;
                    ArmaPrecio.innerText = `$${arma.precio}`;
                    
                });

                // Filtrar los elementos del DOM existentes
                filterExistingArmas(minVal, maxVal);
                
                console.log(data.message);
                // Crear un elemento h1 indicando que no hay armas disponibles
                const divNoArmasMsg = document.createElement('div');
                const noArmasMsg = document.createElement('h1');
                noArmasMsg.textContent = 'No existen armas con ese rango de precios';
                noArmasMsg.className = 'text-center text-white'; // Puedes agregar tus propias clases para estilo
                divNoArmasMsg.appendChild(noArmasMsg);
            }
        }
    }
    const filterExistingArmas = (minVal, maxVal) => {
        const armaItems = document.querySelectorAll('.arma-item');

        armaItems.forEach(item => {
            const precioElement = item.querySelector('.precio');
            const precio = parseFloat(precioElement.textContent.replace('$', ''));

            console.log(precioElement)
            // Filtrar en función del rango de precios y si el precio es diferente de 0
            if (precio >= minVal && precio <= maxVal && precio !== 0) {
                item.style.display = 'block';
            } else {
                item.style.setProperty('display', 'none', 'important');
            }
        });
    };

    rangeInput.forEach(input => {
        input.addEventListener("input", updatePrices);
    });

    // Inicializar la primera carga
    updatePrices();

    
});

