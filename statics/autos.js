const { createApp } = Vue;

createApp({
    data() {
        return {
            autos: [],
            url: 'http://127.0.0.1:5000/autos',
            error: false,
            cargando: true,
            id: 0,
            marca: '',
            modelo: '',
            anio: '',
            patente: '',
            pais_origen: '',
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.autos = data;
                    this.cargando = false;
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        eliminar(auto) {
            const url = this.url + '/' + auto;
            var options = {
                method: 'DELETE',
            };
            fetch(url, options)
                .then(response => response.json())
                .then(response => {
                    location.reload();
                })
        },
        grabar(){
            let auto = {
                marca: this.marca,
                modelo : this.modelo,
                anio: this.anio,
                patente : this.patente,
                pais_origen: this.pais_origen,
            };
            var options = {
                method: 'POST',
                body: JSON.stringify(auto),
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
            .then(function () {
                alert('Se registro el auto');
                window.location.href = './index.html';
            })
            .catch(err => {
                console.error(err);
            });
        }
    },
    
    created() {
        this.fetchData(this.url)
    }


}).mount('#app');