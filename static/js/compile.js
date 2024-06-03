var divMetodos = document.querySelectorAll('.metodo'); //Contém todas as div´s de métodos
var pratique = document.querySelectorAll('.pratique'); //Contém todos os boutton Pratique  
var bio = document.querySelectorAll('.bio');    //Contém todos os button "O que é?"
var dicas  = document.querySelectorAll('.dica');  //Contém todaos os botões acima da ide de código
var metodos = [];  //Array com os métodos
var divConceito = document.getElementById('conceito'); 


divMetodos.forEach(function(el) { //Percorre todos os métodos habilitando o button "O que é?" para as divConceito existente
    var nome_metodo = el.getAttribute('data-target');
    metodos.push(nome_metodo); //preenche o array com métodos existentes
    //inicio
    var children = el.querySelectorAll('.oculto');//busca todos as tag com class ocultar
    //verifica se existe a div conceito do método   
    bio_conceito = divConceito.querySelector("." + nome_metodo); 
    if(bio_conceito){ //Se encontrou uma div com bio-conceito, deixa "O que é? " visível
        children.forEach(function(child) {
            child.classList.remove('oculto');
        })
    }    
});


console.log("metodos",metodos);
pratique.forEach(function(el) {
    el.addEventListener('click', function() {
    // Encontra a div pai mais próximo
    var parentDiv = $(this).closest('div');
    // Obtém o valor do atributo data-target
    var targetId = parentDiv.attr('data-target');
        $('#compilador').data('code', targetId);
        
        $("#myModal #nome_metodo").html(" ( " + targetId +" )");
        
        ide = document.getElementById("ide"); // Recebe o elemento textArea do código
        ide.value += "\n";
        $('#myModal').modal('show');
        /*usando vanila
        var myModal = document.getElementById('myModal');
        var modal = new bootstrap.Modal(myModal);
        modal.show();   */   
    });
 });

 bio.forEach(function(el) {
    el.addEventListener('click', function() {
        // Encontra a div pai mais próximo
        var parentDiv = $(this).closest('div');
        // Obtém o valor do atributo data-target
        var targetId = parentDiv.attr('data-target');
        $('#bio').data('code', targetId); //Talvez seja opcional
        // Buscando um texto de conceito para o método
        var conceito = $('#conceito');
        var metodo = conceito.find("." + targetId); //Busca na div conceito a div específica do método
        // Obtém o conteúdo HTML da div filha
        var metodoContent = metodo.html();
        if(undefined == metodoContent){
            $("#bio").html("<h5 class='text-primary'>Contexto em implementação</h5>");    
        }else{
           $("#bio").html(metodoContent);
        }
        $('#bioModal').modal('show');
    });
 });
 //execute o código em Python
 document.getElementById('run').addEventListener('click', function() {
    //alert('Cliquei em: ' + this.textContent);
    document.getElementById('result').innerHTML = "<pre>...</pre>";    
    var codigo = document.getElementById('ide').value;
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
            alert(data.error);
            document.getElementById('result').innerHTML = "<pre class='error'>" + data.error + "</pre>";
        } else {
            document.getElementById('result').innerHTML = "<pre>" + data.output + "</pre>";
        }
    })
    .catch(error => {
        alert("catch ERRO:");
        console.error('Erro:', error);
        document.getElementById('result').innerHTML = "<pre class='error'>Erro na requisição. Verifique a conexão com o servidor.</pre>";
    });
});
//Limpar a tela do editor de código
document.getElementById('limpa_ide').addEventListener('click', function() {
    document.getElementById("ide").value = "from Bioclass import Bioprof";
    dicas.forEach(function(dica) {
        $(dica).prop('disabled', false);
        //$('#compilador').find('.dica').prop('disabled', true);    
    })
    document.getElementById('result').innerHTML = "<pre>Resultado&raquo;</pre>";    
});

 //Limpar o terminal de resposta ao usuário
 document.getElementById('clear').addEventListener('click', function() {
    document.getElementById("result").innerHTML = "<span class='text-success'>Resultado&raquo;</span>"
});

dicas.forEach(function(dica) {
    dica.addEventListener('click', function() {
        // Busca a targetId da IDE clicada 
        //var targetId = this.getAttribute('data-target');
        var child = document.getElementById(this.getAttribute('id'));
        var metodo = $('#compilador').data('code');
        //alert("Método: " + metodo + "   Linha: " + child.innerText)
        ide = document.getElementById("ide"); // Recebe o elemento textArea do código
        ide.value += "\n" + codigo[metodo][parseInt(child.innerText)-1]; //Adiciona a linha de código referente do botão pressionado
        // Desativa o botão
        $(this).prop('disabled', true);
    });
});

 let codigo = {
    get_seqs : ["seq = Bioprof()","print(seq.get_seqs())","\n#clique no botão Executar"],
    adiciona_seq : ["seq = Bioprof()","seq.adiciona_seq('Genoma1','informação do genoma','ATGCGTAACGTTAGC')","print(seq.get_seqs())","\n#clique no botão Executar",""],
    leiaArquivoFasta:  ["seq = Bioprof()","seq.leiaArquivoFasta('sequencia_dna.fasta')","print(seq.get_seqs())","\n#clique no botão Executar"]
    
 }
 