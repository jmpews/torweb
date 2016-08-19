var gulp = require('gulp'),
    sass = require('gulp-ruby-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    minifycss = require('gulp-minify-css'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    livereload = require('gulp-livereload'),
    webserver = require('gulp-webserver'),
    del = require('del');

gulp.task('scripts', function() {
    return gulp.src('./src/scripts/*.js')
        .pipe(jshint.reporter('default'))
        .pipe(concat('main.js'))
        .pipe(gulp.dest('./dist/js'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest('./dist/js'))
        .pipe(livereload())
        .pipe(notify({ message: 'Scripts task complete' }));
});

gulp.task('styles', function(){
    return sass(['./src/styles/**/*.scss','./src/bootstrap/scss/bootstrap.scss'], { style: 'expanded'})
        .pipe(autoprefixer('last 2 version', 'Safari 5', 'IE 8', 'IE 9', 'Opera 12.1', 'IOS 6', 'android 4'))
        .pipe(gulp.dest('./dist/css'))
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest('./src/css'))
        .pipe(livereload())
        .pipe(notify({ message: 'Styles task complete' }));
})


gulp.task('images', function() {
    return gulp.src('./src/images/**/*')
        .pipe(imagemin({ optimizationLevel: 3, progressive: true, interlaced: true }))
        .pipe(gulp.dest('./dist/images'))
        .pipe(livereload())
        .pipe(notify({ message: 'Images task complete' }));
});

gulp.task('htmls', function() {
    return gulp.src('./src/**/*.html')
        .pipe(gulp.dest('./dist'))
        .pipe(notify({ message: 'Htmls task complete' }));
})

gulp.task('clean', function() {
    // del(['src/assets/css', 'src/assets/img'])
});

gulp.task('watch', function() {
    // Watch .scss files
    gulp.watch('src/bootstrap/scss/*.scss', ['styles']);
    gulp.watch('src/styles/*.scss', ['styles']);
    // Watch .js files
    gulp.watch('src/scripts/*.js', ['scripts']);
    // Watch image files
    gulp.watch('src/images/**/*', ['images']);
    // Watch htmls
    gulp.watch('src/**/*.html', ['htmls']);

    livereload.listen();
    gulp.watch(['dist/**']).on('change', livereload.changed);

});

// Default task
gulp.task('default', ['clean'], function() {
    gulp.start('styles', 'scripts', 'images', 'htmls');
    gulp.start('watch');
});

gulp.task('server', function() {
  gulp.src('src')
    .pipe(webserver({
          livereload: true,
          open: true
        }));
  gulp.start('watch');
});
