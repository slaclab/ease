/**
 * dynamic_forms.js
 *
 * A javascript tool for automating the creation and iteration of Django
 * formsets.
 * 
 * See https://en.wikipedia.org/wiki/JSDoc for documentation guidelines.
 */




class df_controller{
    /**
     * Construct the dynamic form controller by alerting it to the fields that
     * need to be iterated 
     *
     * @constructor
     * @param {string} prefix The string proceeding dynamically allocated
     * fields
     * @param {array} target_fields An array of strings specifying the IDs of
     * the input fields to iterate.
     * @param {array} replacements An array specifying the initial values of the
     * fields when added to the page via the button
     * @param {string} form_section The jquery search term for the element
     * containing the iterated forms. We recommend searching by id using the
     * '#[id-name]' format.
     * @param {string} add_button The jquery search term for the button element
     * that creates more form entries when clicked. We recommend searching by
     * id using the '#[id-name]' format.
     * @param {string} delete_button The jquery search term for a button in the
     * row that deletes the row. We recommend searching by class using the
     * '.[class-name]' format.
     * @this {df_controller}
     */
    constructor(prefix, target_fields, replacements, form_section, add_button, delete_button){
        
        // input arguments 
        this.prefix = prefix;
        this.target_fields = target_fields;
        this.replacements = replacements;
        this.form_section = form_section;
        this.add_button = add_button;
        this.delete_button = delete_button;
        // inform developer of arg length issue
        if (this.target_fields.length != this.replacements.length){
            throw "target_fields and replacments mush have same length";
        }    
        
        // this.next_contents_no designates the next no. for the next row.
        this.next_contents_no = $("input[name="+this.prefix+"-TOTAL_FORMS]").val();
    }

    /**
     * A collection of actions to be completed when the 'add' button is 
     * pressed. Note that unless the .bind method is used when called @this
     * will default to the button element instead of the df_controller
     * instance.
     *
     * @this {df_controller}
     */
    add_trigger_actions(){
        // Collection of actions to take when the "add" button is pressed
        var new_contents = $(this.form_section).children().last().clone();

        // Scan through input fields in row, update fields with new names, IDs
        for (var i = 0; i < this.target_fields.length; i++){
            // construct search term to find correct input element
            find = "[id*=id_"+this.prefix+"-][id*=-"+this.target_fields[i]+"]"

            // seek correct input element   
            var target_element = new_contents.find(find)
            
            // construct new ID
            var update_id = "id_"+this.prefix+
                "-"+this.next_contents_no.toString()+
                "-"+this.target_fields[i]
            
            // update correct input element with new ID
            target_element.attr('id', update_id);

            // construct new name
            var update_name = dfc_prefix+
                "-"+this.next_contents_no.toString()+
                "-"+this.target_fields[i]

            // update correct input element with new name
            target_element.attr('name', update_name);            
            
            // update correct input element with new value 
            new_contents.find(find).val(this.replacements[i]);
        }
    
        // Push new row into live html
        $(this.form_section).append(new_contents);

        var cache = $("input[name="+this.prefix+"-TOTAL_FORMS]").val();
        $("input[name="+this.prefix+"-TOTAL_FORMS]").val(Number(cache)+1);

        this.next_contents_no ++;

        new_contents.find(this.delete_button).click(
            this.delete_trigger_actions.bind(this)
        ); 
    
    }
    /**
     * A collection of actions to be completed when the 'delete' button is
     * pressed. Note that unless the .bind method is used when calld @this will
     * default to the button element instead of the df_controller instance.
     *
     * @param {event} event this is the event of the button press, it is
     * automatically sent when called from the click method
     *
     *
     */
    delete_trigger_actions(event){
        // reject deleting the last remaining entry, there must be at least one
        // trigger at all times
        if ( $("input[name="+this.prefix+"-TOTAL_FORMS]").val() <= 1 ){
            return;
        }

        var button = event.target

        $(button).attr('class',"btn btn-danger text-muted")
        $(button).parentsUntil(this.form_section).last().remove();
          
        var cache = $("input[name="+this.prefix+"-TOTAL_FORMS]").val();
        $("input[name="+this.prefix+"-TOTAL_FORMS]").val(Number(cache)-1);
    }

    prepare_document(){
        $(this.add_button).click(this.add_trigger_actions.bind(this));
        
        $(this.delete_button).click(
            this.delete_trigger_actions.bind(this)
        );
    }

};



function dynamic_form_controller(){
    console.log(dfc_prefix);
    console.log(dfc_fields);
    console.log(dfc_replace);



    var next_contents_no = $('input[name=tg-TOTAL_FORMS]').val();


    $("#add_trigger_btn").click(function(){

        if (dfc_fields.length != dfc_replace.length){
            console.log("ARGUMENT LENGTH ERROR");
        }

        var new_contents = $("#contents_section").children().last().clone();

        
        // new_contents.find("input[id*=id_tg-][id*=-new_name]").attr('id','id_tg-'+next_contents_no.toString()+'-new_name');
        // new_contents.find("input[name*=tg-][name*=-new_name]").attr('name','tg-'+next_contents_no.toString()+'-new_name');
        // new_contents.find("input[name*=tg-][name*=-new_name]").val("");

        // new_contents.find("select[id*=id_tg-][id*=-new_pv]").attr('id','id_tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").attr('name','tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").val(-1);








        for (var i = 0; i < dfc_fields.length; i++){
            find = "[id*=id_"+dfc_prefix+
                "-][id*=-"+dfc_fields[i]+"]"
            update = "id_"+dfc_prefix+
                "-"+next_contents_no.toString()+
                "-"+dfc_fields[i]
            new_contents.find(find).attr('id', update);

            find = "[name*="+dfc_prefix+
                "-][name*=-"+dfc_fields[i]+"]"
            update = dfc_prefix+
                "-"+next_contents_no.toString()+
                "-"+dfc_fields[i]
            new_contents.find(find).attr('name',update);

            find = "[name*="+dfc_prefix+
                "-][name*=-"+dfc_fields[i]+"]"

            new_contents.find(find).val(dfc_replace[i]);
        }

        // new_contents.find("select[id*=id_tg-][id*=-new_pv]").attr('id','id_tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").attr('name','tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").val(-1);


       
        // new_contents
        //     .find("[id*=id_tg-][id*=-new_name]")
        //         .attr('id','id_tg-'+next_contents_no.toString()+'-new_name');
        // new_contents
        //     .find("[name*=tg-][name*=-new_name]")
        //         .attr('name','tg-'+next_contents_no.toString()+'-new_name');
        // new_contents
        //     .find("[name*=tg-][name*=-new_name]")
        //         .val("");

        // new_contents
        //     .find("[id*=id_tg-][id*=-new_pv]")
        //         .attr('id','id_tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents
        //     .find("[name*=tg-][name*=-new_pv]")
        //         .attr('name','tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents
        //     .find("[name*=tg-][name*=-new_pv]")
        //         .val(-1);




        $("#contents_section").append(new_contents);

        var cache = $("input[name=tg-TOTAL_FORMS]").val();
        console.log(cache);
        $("input[name=tg-TOTAL_FORMS]").val(Number(cache)+1);

        next_contents_no ++;
        console.log("click2");


        new_contents.find(".delete-btn").click(delete_handler);


    });



    function delete_handler() {
        if ( $('input[name=tg-TOTAL_FORMS]').val() <= 1 ){
            return;
        }
        //var test = $(this);
        console.log(this);
        console.log($(this));
        $(this).attr('class',"btn btn-danger text-muted")
        //this.innerHTML = "keep this!";
        $(this).parent().parent().remove();
        //console.log($(this)[0].innerHTML); 
        console.log("click_del");
        var cache = $("input[name=tg-TOTAL_FORMS]").val();
        console.log(cache);
        $("input[name=tg-TOTAL_FORMS]").val(Number(cache)-1);
    }


    // handle line deletion

    $(".delete-btn").click(delete_handler);


}
