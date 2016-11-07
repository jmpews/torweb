var gulp = require('gulp'),
    mainBowerFiles = require('main-bower-files'),
    sass = require('gulp-ruby-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    minifycss = require('gulp-minify-css'),
    jshint = require('gulp-jshint'),
    filter = require('gulp-filter'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    livereload = require('gulp-livereload'),
    webserver = require('gulp-webserver'),
    connect = require('gulp-connect');
    del = require('del');
    print = require('gulp-print');
    flatten = require('gulp-flatten');
    util = require('gulp-util');

var distPath='./static/';

var lib= { // 第三方依赖文件
    js: [
    ],
    dist: {
        js: [
            'bower_components/cropper/dist/cropper.min.js',
            'bower_components/jquery/dist/jquery.min.js',
            'bower_components/parsleyjs/dist/parsley.min.js',
            'bower_components/medium-editor/dist/js/medium-editor.min.js',
            'bower_components/remarkable-bootstrap-notify/bootstrap-notify.min.js',
            'bower_components/bootstrap/dist/js/bootstrap.min.js'
        ],
        css: [
            'bower_components/font-awesome/css/font-awesome.min.css',
            'bower_components/medium-editor/dist/css/medium-editor.min.css',
            'bower_components/cropper/dist/cropper.min.css',
        ],
        path: [
            'bower_components/summernote/dist/font',
            'bower_components/parsleyjs/dist/i18n'
        ]

    },
    scss: [
        'src/lib/bootstrap/scss/bootstrap.scss'
    ]
};

// // 过滤文件, 根据bower.json自动生成
// var filterByExtension = function(extension) {
//     return filter(function(file) {
//         var f = file.path.match(new RegExp('.' + extension + '$'));
//         util.log(f);
//         return f;
//     });
// };
//
// // 将bower安装的第三方包，存储到dist/lib目录下
// gulp.task('bower', function() {
//     var mainFiles = mainBowerFiles();
//     var cssFilter = filterByExtension('css');
//     var jsFilter = filterByExtension('js');
//     return gulp.src(mainFiles, { base: '' })
//         .pipe(cssFilter)
//         .pipe(gulp.dest(distPath+'/lib'))
//         .pipe(rename({suffix: '.min'}))
//         .pipe(minifycss())
//         .pipe(gulp.dest(distPath+'/lib'))
//         .pipe(notify({ message: 'Bowers task complete' }));
// });

gulp.task('copy', function () {
    gulp.src(lib.dist.js, {})
    // without file dir path
        .pipe(rename({dirname: ''}))
        .pipe(gulp.dest(distPath + '/assets/js'));

    gulp.src(lib.dist.css, {})/*{cwd: 'bower_components/**'}*/
    // without file dir path
        .pipe(rename({dirname: ''}))
        .pipe(gulp.dest(distPath + '/assets/css'));

});

//deal with custom scipt
gulp.task('scripts', function() {
    return gulp.src(['./src/scripts/index.js', './src/scripts/base.js', './bower_components/js-url/url.js'])
        .pipe(jshint.reporter('default'))
        .pipe(concat('main.js'))
        .pipe(gulp.dest(distPath+'/assets/js'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest(distPath+'/assets/js'))
        .pipe(notify({ message: 'Scripts task complete' }));
});

//deal with custom styles
gulp.task('styles', function(){
    return sass(['./src/styles/index.color4.scss', './src/styles/blog.scss'], { style: 'expanded'})
        .pipe(autoprefixer('last 2 version', 'Safari 5', 'IE 8', 'IE 9', 'Opera 12.1', 'IOS 6', 'android 4'))
        .pipe(gulp.dest(distPath+'/assets/css'))
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest(distPath+'/assets/css'))
        .pipe(notify({ message: 'Styles task complete' }));
});

gulp.task('images', function() {
    return gulp.src('./src/images/**/*')
        .pipe(imagemin({ optimizationLevel: 3, progressive: true, interlaced: true }))
        .pipe(gulp.dest(distPath+'/assets/images'))
        .pipe(notify({ message: 'Images task complete' }));
});

gulp.task('htmls', function() {
    return gulp.src('./templates/**/*.html')
        .pipe(gulp.dest(distPath))
        .pipe(notify({ message: 'Htmls task complete' }));
});



gulp.task('clean', function() {
    // del(['src/assets/css', 'src/assets/img'])
});

gulp.task('watch', function() {
    // 监听文件变化
    gulp.watch('src/styles/*.scss', ['styles']);
    gulp.watch('src/lib/bootstrap/scss/*.scss', ['styles']);
    gulp.watch('src/scripts/index.js', ['scripts']);
    gulp.watch('src/scripts/base.js', ['scripts']);
    gulp.watch('src/scripts/plugin.js', ['scripts-plugin']);
    gulp.watch('src/images/**/*', ['images']);
});

// Default task
gulp.task('default', ['clean'], function() {
    gulp.run('styles', 'scripts', 'images', 'copy');
    gulp.run('watch')
});

