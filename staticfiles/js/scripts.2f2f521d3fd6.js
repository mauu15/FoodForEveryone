// Funzione per aprire o chiudere il menu dell'account
    function toggleAccountMenu() {
        var menu = document.getElementById('accountMenu');
        menu.classList.toggle('show');
    }

    // Chiudi il menu se l'utente clicca fuori da esso
    window.onclick = function(event) {
        if (!event.target.matches('.nav-link')) {
            var dropdowns = document.getElementsByClassName('dropdown-menu');
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }


    // Funzione per rimuovere una ricetta dai preferiti
$(document).ready(function() {
        $('.remove-favorite-btn').click(function(e) {
            e.preventDefault();
            var recipeId = $(this).data('recipe-id');

            $.ajax({
                type: 'POST',
                url: '/favorites/' + recipeId + '/remove/',
                data: {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function(data) {
                    // Rimuovi la ricetta dalla visualizzazione
                    $('#recipe-' + recipeId).remove();
                },
                error: function(xhr, status, error) {
                    console.error(error);
                }
            });
        });
    });