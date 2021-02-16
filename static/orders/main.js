var CSS_COLOR_NAMES = ["Pink", "Green", "Red", "Blue", "Orange", "Brown", "Crimson", "DarkBlue", "Gray", "Grey"]



function bindOrderEvents() {
    $(".note").on("click", function(event){ 
                            var customer_note = $(this).closest('tr').children('td:first').text();
                            var note_val = $(this).text();
                            $('#changenotedialog').dialog("option", "title", "Change Note: "+ customer_note);
                            $('#changenotedialog').dialog("option","position",{my:"left top", at:"left top", of:event.target});
                            $("#changenotedialog").dialog("open"); 
                            $("#changenotedialog #id_note").val(note_val);
                            $("#changenoteform>#customer").val($(this).closest("tr").attr("customer"));
                            });
    $(".PO").on("click", function(event){ 
                            var PO_name = $(this).text();
                            var customer_po = $(this).closest('tr').children('td:first').text();
                            $('#changePOdialog').dialog("option", "title", "Change PO: "+ customer_po);
                            $('#changePOdialog').dialog("option","position",{my:"left top", at:"left top", of:event.target});
                            $("#changePOdialog").dialog("open"); 
                            $("#changePOdialog #id_PO").val(PO_name);
                            $("#changePOform>#customer").val($(this).closest("tr").attr("customer"));
                            });
    $(".customer").on("click", function(event){ 
                            var customer_name = $(this).text();
                            $("#changepallettedialog").dialog('option', 'title', 'Change Pallette: '+customer_name);
                            $('#changepallettedialog').dialog("option","position",{my:"left top", at:"left top", of:event.target});
                            $("#changepallettedialog").dialog("open"); 
                            $("#changepalletteform>#customer").val($(this).closest("tr").attr("customer"));
                            });

    $(".order").on("click",function(event){
        var customer_order = $(this).closest('tr').children('td:first').text();
        var order_name = $(this).text();
        targ = $(event.target);
        if(targ.attr('recurring') == "True") {
            $("#changeorderform").attr('recurring','true');
            $("#changeorderform_warning").show();
        } else {
            $("#changeorderform_warning").hide();
            $("#changeorder_warning").show();
        }

        $('#changeorderdialog').dialog("option","position", {my:"left top", at:"left top", of:event.target});
        $('#changeorderdialog').dialog("option", "title", order_name+'-'+ customer_order);

        var deets = event.target.innerText;
        var spl = deets.split('|');
        var price = spl[1] || '';
        xspl = spl[0].split('x');
        var size = xspl[1] || '';
        var quantity = xspl[0] || '';

        $('#changeorderdialog #id').val(event.target.id);
        $('#changeorderdialog #id_size').val(size);
        $('#changeorderdialog #id_special_unit_price').val(price);
        $('#changeorderdialog #id_quantity').val(quantity);
        $("#changeorderdialog").dialog("open");        

    });
    function grab_selected() {
    var tasks = [];
    $("#catselect>option:selected").each(function() {
        tasks.push(this.text);
    });
    return tasks;
}

    $("#catselect").on("change",function(){

        var categories = grab_selected();
        $.ajax({
                    url: "/orders"+ date.substring(5,10) + "/" + date.substring(0,5),
                    type: "POST",
                    data: {csrfmiddlewaretoken: csrftoken, 'categories[]': categories},
                    dataType: "HTML",
                    error: function(msg){
                        alert(msg.statusText);
                        return msg;
                    },
                    success: function(html){
                                            $("#container").html(html);
                                            bindOrderEvents();
                                           }
                   });

    });


    $("#palletteselect").on("change",function(){
                $("#ordertable tr").show(); 
                $("#ordertable td, #totalstable td").css("display","table-cell");
                $("#palletteselect>option:not(:selected)").each(function(){
                                                                              hideme = "." + $(this).text(); 
                                                                              $(hideme).hide()
                totaloftotals = 0;   
                                                                          });
                customers = $("#ordertable tr:visible");
                $('#customercount').html(function() {return 'Customers:'+ (customers.length-1).toString()});

                totals = {};
                for(x in theproducts) { 
                    p = theproducts[x]; 
                    totals[p] = {}; 
                    orders = $('[product="' + p + '"]:visible');
                    if(orders.length) {
                        orders.each(
                            function(){
                            totaloftotals += parseInt($(this).attr("quantity"));          
                            totals[p][$(this).attr("key")] = parseInt($(this).attr("quantity")) 
                                                           + (totals[p][$(this).attr("key")] || 0);
                            }
                        );
                    } else {
                        $("#ordertable tr, #totalstable tr").each(function(){$(this).children("td")[+x+1].style.display="None";});
                    }
                }

                for(key in totals){
                    html = ''; 
                    for(key2 in totals[key]){
                        html+='<p>' + totals[key][key2] + key2 + '</p>';
                    }
                    
                    $('#' + key).html(html);
                }
                $('#totaloftotals').html('<p>' + totaloftotals + '</p>');
 
            });

    $(".date").val($('#datepicker').datepicker().val());
}


function showRecurring() {
    $.post({
        url:"/orders/get_recurring_orders",
        data: { csrfmiddlewaretoken:csrftoken },
        dataType: "HTML",
        error: function(msg){
            alert(msg.statusText);
            return msg;
        },
        success: function(html){
            $("#viewrecurringdialog .container").html(html); $("#viewrecurringdialog").dialog("open");
            $(".deleterecurringorderbutton").on("click", function() { 
                $.post({
                    url:"/orders/delete_recurring_order",
                    data: {
                        csrfmiddlewaretoken:csrftoken,
                        id: $(this).closest("tr").attr("id"),
                        date: $("#datepicker").datepicker().val(),
                        deleterecurring: 'true'
                    },
                    success:function(){showRecurring(); alert("order deleted!"); }
                });
            });
        }
    });
    
}

function updateTable() {
            date=$("#datepicker").datepicker().val();
            $("#printdate").children('span').html(date);
            $(".ui-state-highlight").removeClass("ui-state-highlight");
            $.ajax({
                    url: "/orders"+ date.substring(5,10) + "/" + date.substring(0,5),
                    type: "POST",
                    data: {csrfmiddlewaretoken: csrftoken},
                    dataType: "HTML",
                    error: function(msg){
                        alert(msg.statusText);
                        return msg;
                    },
                    success: function(html){
                                            $("#container").html(html);
                                            bindOrderEvents();
                                           }
                   });
} 


$(window).ready(function() {


     
    $('body').show();


    $( "#addorderform>#id_product" ).autocomplete({source:allproducts});
    $( "#addorderform>#id_customer" ).autocomplete({source:allcustomers});
    $( "#addorderform_pallette, #changepalletteform>#id_pallette" ).autocomplete({source:CSS_COLOR_NAMES});

    $("#id_recurring").on("change",function(){$("#id_frequency, #id_frequency_label, #recurring_days").toggle()});

    $('.dialog').dialog({autoOpen:false, modal:true});  
    $('#addorderdialog').dialog({autoOpen:false, modal: true, width: 350});
    $('#viewhistorydialog').dialog({autoOpen:false, modal: true, width: 1250, height: 550});
    $('#viewrecurringdialog').dialog({autoOpen:false, modal: true, width: 1250, height: 550});
    $('#viewrecurringdialog').on('dialogclose',function(){location.reload();});

    $("#datepicker").datepicker({showOtherMonths: true,
            selectOtherMonths: true, onSelect: updateTable});

    date = $("#datepicker").datepicker().val();
    $("#printdate").children('span').html(date);

    $("#deleteorderbutton").on("click", function() {
        updateTable(); $('#id_note').val('');
        $.post({
            url:"/orders/delete_order",
            data: {
                csrfmiddlewaretoken:csrftoken, 
                id: $('#changeorderdialog #id').val(),
                date: $('#datepicker').datepicker().val(),
                recurring: $('#changeorderdialog').attr('recurring') ? 'True' : ''
            },
            success:function(){$("#changeorderdialog").dialog("close");  console.log($('#id_note').val()); updateTable(); $('#id_note').val('');}
        })
    });

    $("#addorderbutton").on("click",function() {$('#id_note').val(''); $("#addorderform .deleteitembutton:not(.hidden)").trigger("click"); $("#addorderform").trigger('reset'); $("#addorderdialog").dialog("open"); $("#id_recurring").attr('checked',false); $("#id_frequency, #id_frequency_label, #recurring_days").hide();})

    $("#viewhistorybutton").on("click", function() { 
                               $.post('/orders/get_history',{ csrfmiddlewaretoken:csrftoken, date: $("#datepicker").datepicker().val()})            
                                .done( function(html){$("#viewhistorydialog .container").html(html); $("#viewhistorydialog").dialog("open");})
                                .fail( function(xhr, textStatus, errorThrown) { alert(xhr.responseText);});
                             })

    $("#viewrecurringbutton").on("click", showRecurring);
                 
    $("#logoutbutton").on("click", function() { window.location.href = "/accounts/logout/"; });


    $("#deleteitembutton").on("click",function(){ $(this).nextUntil("#additembutton,.deleteitembutton").remove(); $(this).remove();$('#addorderform_note').val('');$('#id_note').val('');})

    $("#additembutton").on("click",function() {
                                                $("#id_note").val('');
                                                $("#deleteitembutton").clone(true).insertBefore("#additembutton").removeClass("hidden");
                                                $("#id_product").clone().attr("placeholder","Product").val("").insertBefore("#additembutton").autocomplete({source:allproducts}).focus();
                                                $("#id_quantity").clone().attr("placeholder","Quantity").val("").insertBefore("#additembutton");
                                                $("#id_size").clone().attr("placeholder","Size").val("").insertBefore("#additembutton");
                                                $("#id_special_unit_price").clone().attr("placeholder","Special Price").val("").insertBefore("#additembutton");
                                                $("<br>").insertBefore("#additembutton");
                                               });
     $("#addorderform").submit(
         function(event) { 
              event.preventDefault(); 
              data = $('#addorderform').serializeArray()
               .concat({name:'csrfmiddlewaretoken',value:csrftoken},{name:'date',value:$('#datepicker').datepicker().val()});
              
              $.post('/orders/add_order',data)
               .done( function(){$("#addorderdialog").dialog("close"); updateTable();})
               .fail( function(xhr, textStatus, errorThrown) { alert(xhr.responseText);});
         }
     );

    $("#changepalletteform").submit(
        function(event) {
            event.preventDefault();
            data = $('#changepalletteform').serializeArray()
             .concat({name:'csrfmiddlewaretoken',value:csrftoken},{name:'date',value:$('#datepicker').datepicker().val()});
            
            $.post('/orders/change_pallette',data)
             .done( function(){$("#changepallettedialog").dialog("close"); updateTable(); })
             .fail( function(xhr, textStatus, errorThrown) { alert(xhr.responseText);});
         }
     )

    $("#changePOform").submit(
        function(event) {
            event.preventDefault();
            data = $('#changePOform').serializeArray()
             .concat({name:'csrfmiddlewaretoken',value:csrftoken},{name:'date',value:$('#datepicker').datepicker().val()});
            
            $.post('/orders/change_po',data)
             .done( function(){$("#changePOdialog").dialog("close"); updateTable(); $('#id_PO').val('');})
             .fail( function(xhr, textStatus, errorThrown) { alert(xhr.responseText);});
         }
     )

    $("#changenoteform").submit(
        function(event) {
            event.preventDefault();
            data = $('#changenoteform').serializeArray()
             .concat({name:'csrfmiddlewaretoken',value:csrftoken},{name:'date',value:$('#datepicker').datepicker().val()});
            
            $.post('/orders/change_note',data)
             .done( function(){$("#changenotedialog").dialog("close"); updateTable(); $('#id_note').val('');})
             .fail( function(xhr, textStatus, errorThrown) { alert(xhr.responseText);});
        }
     )
     
     $("#changeorderform").submit(
        function(event) {
            event.preventDefault();
            data = $('#changeorderform').serializeArray()
             .concat({name:'csrfmiddlewaretoken',value:csrftoken},{name:'date',value:$('#datepicker').datepicker().val()});
            
            $.post('/orders/change_order',data)
             .done( function(){$("#changeorderdialog").dialog("close"); updateTable();})
             .fail( function(xhr, textStatus, errorThrown) { alert(xhr.responseText);});
        }
     );

    bindOrderEvents(); 



     
});
