;( function( $, window, document, undefined ) {
    "use strict";

    var filters = {
        categories: '*',
        tags: [ ]
    };


    /** Helper functions */

    /**
     * function to normalize text
     * @param {string} text
     */
    function normalizeText(text) {
        return text.toLocaleLowerCase().replace(' ', '_');
    }

    /**
     * Show all the grid item tiles
     */
    function showAll() {
        $('.grid-item').show();
    }

    /**
     * Hide all teh grid item tiles
     */
    function hideAll() {
        $('.grid-item').hide();
    }

    /**
     * Sets the category value to the filters
     * @param {string} category
     */
    function setFilterCategory(category) {
        filters.categories = normalizeText(category);
    }

    /**
     * Sets the tag value to the filters, dedupes values as well
     * @param {string[]} tag 
     */
    function setFilterTags(tags) {
        filters.tags = $.map( tags, function( elem ) {
            return '.tag-' + normalizeText(elem);
        });
    }

    function filterItems() {
        hideAll(); // reset all objects

        // hide everything that matches the category filter
        var focusedItems;

        if( filters.categories !== '*' ) {
            focusedItems = $('.grid-item' + filters.categories);
        } else {
            focusedItems = $('.grid-item');
        };
        
        // show only the tags which we are filtering on
        $.each(filters.tags, function( index, value ) {
            focusedItems = focusedItems.filter(value);
        });

        focusedItems.show();
        
    }

    /** Initializer functions */

    function initCategories() {
        $('.filter-btn').click(function(evt) {
            var filterValue = evt.target.getAttribute('data-filter-value');
            setFilterCategory(filterValue);
            filterItems();
        });
    }

    function initSelect() {
        $('select').select2({
            placeholder: 'Filter by tag',
        });
        $('select').on("select2:select", function (e) { 
            var tags = $('select').val();
            setFilterTags(tags);
            filterItems();
        });
        $('select').on("select2:unselect", function (e) { 
            var tags = $('select').val();
            setFilterTags(tags);
            filterItems();
        });

    }

    /** Main */

    function main(){
        initCategories();
        initSelect();
    } 
    main();

}) ( jQuery, window, document );