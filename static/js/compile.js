var pratique = document.querySelectorAll('.pratique');   
var execute = document.querySelectorAll('.executar');   
var limpar = document.querySelectorAll('.limpar');   

pratique.forEach(function(el) {
    el.addEventListener('click', function() {
        // Remove a classe 'active' de todas as divs
        document.querySelectorAll('.ide').forEach(function(div) {
            div.classList.remove('active');
        });
      
        // Adiciona a classe 'active' à div correspondente ao botão clicado
        var targetId = this.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
    });
 });

execute.forEach(function(el) {
    el.addEventListener('click', function() {
      //alert('Cliquei em: ' + this.textContent);
      var codigo = document.getElementById('code').value;
      fetch('/execute', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ code: codigo })
      })
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              document.getElementById('resultado').innerHTML = "<pre class='error'>" + data.error + "</pre>";
          } else {
              
              document.getElementById('resultado').innerHTML = "<pre>" + data.output + "</pre>";
          }
      })
      .catch(error => {
          console.error('Erro:', error);
          document.getElementById('resultado').innerHTML = "<pre class='error'>Erro na requisição. Verifique a conexão com o servidor.</pre>";
      });
    });
  });


  limpar.forEach(function(el) {
    el.addEventListener('click', function() {
      //alert('Cliquei em: ' + this.textContent);
      document.getElementById('resultado').innerHTML = "";
    })  
  });
