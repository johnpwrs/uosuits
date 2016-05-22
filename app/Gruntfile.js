module.exports = function(grunt) {

  grunt.initConfig({
    jshint: {
      files: ['Gruntfile.js', './src/js/*.js'],
      options: {
        globals: {
          jQuery: true
        }
      }
    },
    watch: {
      files: ['<%= jshint.files %>', './src/views/*.html', './src/css/*.css'],
      tasks: ['jshint', 'concat', 'copy']
    },
    concat: {
      js: {
        src: ['./src/js/*.js'],
        dest: './dist/js/main.js'
      },
      css: {
        src: ['./src/css/*.css'],
        dest: './dist/css/main.css'
      }
    },
    copy: {
      views: {
        expand: true,
        cwd: 'src/', 
        src: 'views', 
        dest: './dist/'
      },
      images: {
        expand: true,
        cwd: 'src/', 
        src: 'img', 
        dest: './dist/'
      },
      vendor: {
        expand: true,
        cwd: 'src/', 
        src: 'vendor', 
        dest: './dist/'
      },
      css: {
        expand: true,
        cwd: 'src/css/', 
        src: '**', 
        dest: './dist/css/'
      },
      fonts: {
        expand: true,
        cwd: 'src/fonts/', 
        src: '**', 
        dest: './dist/fonts/'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['watch']);

};
