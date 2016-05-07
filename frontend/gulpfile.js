var gulp = require('gulp'),
    less = require('gulp-less'),
    sass = require('gulp-ruby-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    minifycss = require('gulp-minify-css'),
    eslint = require('gulp-eslint');
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    del = require('del');

gulp.task('scripts', function() {
  return gulp.src('src/scripts/*.js')
    .pipe(eslint.formatEach('compact', process.stderr))
    .pipe(concat('main.js'))
    .pipe(gulp.dest('src/assets/js'))
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gulp.dest('src/assets/js'))
    .pipe(notify({ message: 'Scripts task complete' }));
});

gulp.task('styles', function(){
    return sass(['./src/bootstrap/scss/bootstrap.scss','./src/styles/index.scss'])
    .pipe(autoprefixer('last 2 version', 'Safari 5', 'IE 8', 'IE 9', 'Opera 12.1', 'IOS 6', 'android 4'))
    .pipe(gulp.dest('src/assets/css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gulp.dest('src/assets/css'))
    .pipe(notify({ message: 'Styles task complete' }));
})


gulp.task('images', function() {
  return gulp.src('src/images/**/*')
    .pipe(imagemin({ optimizationLevel: 3, progressive: true, interlaced: true }))
    .pipe(gulp.dest('src/assets/img'))
    .pipe(notify({ message: 'Images task complete' }));
});

gulp.task('clean', function() {
    del(['src/assets/css', 'src/assets/img'])
});

gulp.task('watch', function() {
  // Watch .scss files
  gulp.watch('src/bootstrap/scss/*.scss', ['styles']);
  gulp.watch('src/styles/*.scss', ['styles']);
  // Watch .js files
  gulp.watch('src/scripts/*.js', ['scripts']);
  // Watch image files
  gulp.watch('src/images/**/*', ['images']);
});

// Default task
gulp.task('default', ['clean'], function() {
    gulp.start('styles', 'scripts', 'images');
    gulp.start('watch');
});


