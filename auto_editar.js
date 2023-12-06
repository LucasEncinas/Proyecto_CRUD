console.log(location.search); // Lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);

const { createApp } = Vue;

createApp({
    data() {
        return {
            id: 0,
            marca: '',
            modelo: '',
            anio: '',
            patente: '',
            pais_origen: '',
            url: 'http://localhost:5000/autos/' + id,
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.id = data.id;
                    this.marca = data.marca;
                    this.modelo = data.modelo;
                    this.anio = data.anio;
                    this.patente = data.patente;
                    this.pais_origen = data.pais_origen;
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        modificar() {
            let auto = {
                marca: this.marca,
                modelo: this.modelo,
                anio: this.anio,
                patente: this.patente,
                pais_origen: this.pais_origen,
            };
            var options = {
                body: JSON.stringify(auto),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado");
                    window.location.href = "./index.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar");
                });
        }
    },
    created() {
        this.fetchData(this.url);
    },
}).mount('#app');