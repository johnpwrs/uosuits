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
      files: ['<%= jshint.files %>', './src/views/*.html'],
      tasks: ['concat', 'copy']
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
        cwd: 'src/views/', 
        src: '**', 
        dest: './dist/views/'
      },
      images: {
        expand: true,
        cwd: 'src/img/', 
        src: '**', 
        dest: './dist/img/'
      },
      vendor: {
        expand: true,
        cwd: 'src/vendor/', 
        src: '**', 
        dest: './dist/vendor/'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['watch']);

};
