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
        dest: './static/js/main.js'
      },
      css: {
        src: ['./src/css/*.css'],
        dest: './static/css/main.css'
      }
    },
    copy: {
      views: {
        expand: true,
        cwd: 'src/views/', 
        src: '**', 
        dest: './static/views/'
      },
      images: {
        expand: true,
        cwd: 'src/img/', 
        src: '**', 
        dest: './static/img/'
      },
      vendor: {
        expand: true,
        cwd: 'src/vendor/', 
        src: '**', 
        dest: './static/vendor/'
      },
      css: {
        expand: true,
        cwd: 'src/css/', 
        src: '**', 
        dest: './static/css/'
      },
      fonts: {
        expand: true,
        cwd: 'src/fonts/', 
        src: '**', 
        dest: './static/fonts/'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['jshint', 'concat', 'copy', 'watch']);
  grunt.registerTask('build', ['jshint', 'concat', 'copy']);

};
