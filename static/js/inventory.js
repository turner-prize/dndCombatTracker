$("#inventoryTable tr").on('click', function() {
    $(this).addClass('selected').siblings().removeClass('selected'); 
    });
    
$('#removeItem').on('click', function() {
    var inam = $('#inventoryTable tr.selected > .iName').html();
    var iquan = $('#inventoryTable tr.selected > .iQuant').html();
    var URL ="/inventory/remove"

    req = $.ajax({
            url : URL,
            type : 'POST',
            data : { item : inam, quantity : iquan }
        });

        req.done(function(data) {
            $('.inventoryPage').html(data);
        });
    });
    
    
$('#submitAddItemForm').on('click', function() {
    var URL ="/inventory/add"
    var inam = $('#xitem').val();
    var iquan = $('#xquantity').val();
    
    req = $.ajax({
            url : URL,
            type : 'POST',
            data : { item : inam, quantity : iquan }
        });
   
    req.done(function(data) {
        $('.inventoryPage').html(data);
        });
    });