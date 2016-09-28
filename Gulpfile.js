/* Needed gulp config */
var gulp = require('gulp');
var sass = require('gulp-sass');
var scsslint = require('gulp-scss-lint');
var cache = require('gulp-cached');
var autoprefixer = require('gulp-autoprefixer');
var neat = require('node-neat');
var minifycss = require('gulp-minify-css');
var concat = require('gulp-concat');
var plumber = require('gulp-plumber');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var uncss = require('gulp-uncss');
var jshint = require('gulp-jshint');
var htmlhint = require("gulp-htmlhint");
var concat = require('gulp-concat');

/* Html lint */
gulp.task('html-lint', function () {
    gulp.src('templates/*.html')
    .pipe(htmlhint())
    .pipe(htmlhint.reporter())
    .pipe(reload({stream:true}));
});

/* Js lint */
gulp.task('js-lint', function() {
  return gulp.src('static/js/main.js')
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
});

/* Sass lint */
gulp.task('scss-lint', function() {
  return gulp.src('sass/*.scss')
    .pipe(cache('scsslint'))
    .pipe(scsslint());
});

/* Js task */
gulp.task('js-concat', function() {
  return gulp.src([
      'static/bower_components/jquery/dist/jquery.min.js',
      'static/bower_components/jscroll/jquery.jscroll.min.js',
      'static/bower_components/materialize/dist/js/materialize.min.js',
      'static/js/main.js'
    ])
    .pipe(concat('all.js'))
    .pipe(gulp.dest('static/js'))
    .pipe(reload({stream:true}));
});

/* Sass task */
gulp.task('sass', function () {
    gulp.src('sass/style.scss')
    .pipe(plumber())
    .pipe(sass({
        includePaths: ['scss'].concat(neat)
    }))
    .pipe(autoprefixer({
        browsers: ['last 3 versions'],
        cascade: false
    }))
    .pipe(uncss({
        html: ['templates/*.html'],
        ignore: [new RegExp('.active$')]
    }))
    .pipe(minifycss())
    .pipe(gulp.dest('static/css'))
    /* Reload the browser CSS after every change */
    .pipe(reload({stream:true}))
});

/* Prepare Browser-sync for localhost */
gulp.task('browser-sync', function() {
    browserSync.init(['static/css/*.css', 'static/js/*.js'], {
        proxy: '127.0.0.1:8000'
    });
});

/* Watch scss, js and html files, doing different things with each. */
gulp.task('default', ['scss-lint', 'sass', 'browser-sync'], function () {
    /* Watch scss, run the sass task on change. */
    gulp.watch(['sass/*.scss', 'sass/**/*.scss'], ['scss-lint', 'sass'])
    /* Watch app.js file, run the scripts task on change. */
    gulp.watch(['static/js/*.js'], ['js-lint', 'js-concat'])
    /* Watch .html files, run the bs-reload task on change. */
    gulp.watch(['templates/*.html'], ['html-lint']);
});
