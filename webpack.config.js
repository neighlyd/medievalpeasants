// tutorial used to create this file, as well as integrate webpack and React into project:
// http://geezhawk.github.io/using-react-with-django-rest-framework
//set up and require our dependencies
var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    // the base directory (absolute path) for resolving the entry option.
    context: __dirname,
    // the entry point we created earlier. Note that './' means the current directory. You do not have to specify extensions
    // now, because you will specify them later in the 'resolve' section.
    entry: [
        './assets/js/index',
        ],

    output: {
        // where you want your compiled bundle to be stored
        path: path.resolve('./assets/bundles/'),
        // naming convention that webpack should use for your files.
        filename: '[name]-[hash].js',
        },

    plugins: [
        // tells webpack where to store data about your bundles.
        new BundleTracker({filename: './webpack-stats.json'}),

        // makes jQuery available in every module
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        })
    ],

    module: {
        loaders: [
            // a regex that tells webpack to use the following loaders on all .js and .jsx files
            {test: /\.jsx?$/,
                // we definitely don't want babel to transpile all the files in node_modules, as that would take a long
                // time.
                exclude: /node_modules/,
                // tell webpack to use babel loader, then pass to react-hot loader
                use:[{
                    loader: 'babel-loader',
                    options: {
                        babelrc: false,
                        // specify that we will be dealing with React code.
                        presets: [
                            'react',
                            'es2015',
                        ]
                    }
                }]
            },
            {test: /\.css?$/,
                // exclude node_modules.
                exclude: /node_modules/,
                use:['style-loader', 'css-loader']

            }
        ]
    },

    resolve: {
        // The tutorial used an older version of Webpack which required calling resolve.modulesDirectories. Webpack 3.5.6
        // does not have this function. Instead, it uses resolve.modules, which defaults to 'node_modules, and thus can be
        // left blank.

        // tell webpack which extensions to use to resolve modules. Webpack 3.5.6 defaults to .js and .json. Because we
        // are using React, we need to include .jsx here.
        extensions: ['.js', '.jsx']

    }
}