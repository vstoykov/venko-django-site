/*globals jQuery, window */
/*jslint plusplus: true, nomen: true, regexp: true, vars: true */

(function ($) {
    "use strict";

    function Gallery (data) {
      this.index = data.index;
      this.slug = data.slug;
      this.url = data.url;
      this.title = data.title;
      this.$element = null;
      this.pictures = $.map(data.pictures, function (name) {
        return {
          src: this.url + name,
          title: name.replace(/[_\-]/g, ' ').split('.')[0],
          thumb: {
            src: this.url + 'thumbs/' + name
          }
        };
      }.bind(this));
    };

    Gallery.prototype.getThumbnailUrl = function () {
      return this.pictures[0].thumb.src;
    }

    Gallery.prototype.getElement = function () {
        if (!this.$element) {
          this.$element = this.render().hide().insertAfter(this.index.$element);
          $('a', this.$element).venobox();
        }
        return this.$element;
    };

    Gallery.prototype.render = function () {
      return $('<div>', {
        'class': 'card-columns',
        'id': this.url,
      }).append(
        $.map(this.pictures, this.renderPicture.bind(this))
      );
    }

    Gallery.prototype.renderPicture = function (picture) {
      return $('<figure>').append(
        $('<a>', {
          'class': "card img-fluid",
          'href': picture.src,
          'title': picture.title,
          'data-gall': this.slug,
        }).append(
          $('<img>', {
            'src': picture.thumb.src,
            'alt': picture.title,
            'class': 'card-img-top'
          })
        )
      );
    }

    function Galleries (options) {
      this.options = options || {};
      this.items = [];
      this.$element = $(this.options.element);
      this.$title = $(this.options.title);
      this.listIndexTitle = this.$title.text();
      this.$breadcrumb = $(this.options.breadcrumb);
      this.$backButtons = $(this.options.backButtons);

      this.$backButtons.on('click', function(e) {
        this.listIndex()
        e.preventDefault();
      }.bind(this));

      this.$element.on('click', 'a[data-gallery]', function (e) {
        var $card = $(e.currentTarget).closest('.card');
        this.showGallery($card.data('gallery'));
        e.preventDefault();
      }.bind(this));
    };

    Galleries.prototype.loadData = function () {
      $.ajax({
        url: this.options.index,
        context: this,
        dataType: 'json',
      }).done(function (response) {
        this.items = $.map(response, function (data, slug) {
          return new Gallery({
            index: this,
            slug: slug,
            url: this.options.url + slug + '/',
            title: data.title,
            pictures: data.pictures
          });
        }.bind(this));
        this.render();
        this.listIndex();
      });
    };

    Galleries.prototype.render = function () {
      this.$element.html('');
      var elements = $.map(this.items, this.renderGaleryCard);
      this.$element.append(elements);
    }

    Galleries.prototype.renderGaleryCard = function(gallery) {
      var url = '#' + gallery.url;
      var $card = $('<div class="card">').append(
        $('<a>', {
          'href': url,
          'data-gallery': gallery.slug
        }).append(
          $('<img>', {
            'src': gallery.getThumbnailUrl(),
            'class': 'card-img-top',
          })
        )
      ).append(
        $('<div class="card-body text-center">').append(
          $('<a>', {
            'href': url,
            'class': 'h4',
            'data-gallery': gallery.slug
          }).text(gallery.title)
        )
      ).data('gallery', gallery);
      return $card;
    }

    Galleries.prototype.showGallery = function(gallery) {
      var $el = gallery.getElement();
      this.$element.hide();
      $el.fadeIn('slow');
      this.$title.text(gallery.title);
      $('.breadcrumb-item.active', this.$breadcrumb).text(gallery.title);
      this.$breadcrumb.css('visibility', 'visible');
      this.$backButtons.css('visibility', 'visible');
    }
    Galleries.prototype.listIndex = function (e) {
      var loadedGalleries = $.map(this.items, function(item) {
        return item.$element ? item.$element.get(0) : null;
      }).filter(Boolean);
      $(loadedGalleries).hide();
      this.$element.fadeIn('slow');
      this.$title.text(this.listIndexTitle);
      this.$breadcrumb.css('visibility', 'hidden');
      this.$backButtons.css('visibility', 'hidden');
    };

    window.Galleries = Galleries;
})(jQuery);
