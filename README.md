# REPL Gallery

This is a handy starter point for generating a gallery of student's repls from replit.

You can download it to get started up the top there ^.

## Getting setup

You'll need to be a little bit comfortable with a terminal to use this. You'll also
need `python3` and `npm`.

You can get python on the [official website](https://www.python.org/).

NPM comes with NodeJS, you can install it [from their website](https://nodejs.org/en/).

Open your terminal and navigate to this directory. Start by installing dependencies:

```
$ npm install
```

You can then run the website locally with:

```
$ npm run dev
```

Visit [http://localhost:8000](http://localhost:8000/) to view it. It should just be a blank gallery.

## Adding your data

To add your data you'll first need to export it to a csv like `data.csv`. You can store it anywhere but this directory is easy. If you're using Excel or Google Sheets there should be an export option for CSV. It should "just work".

Your data should have a column with replit project URLs. This is just the URL the user works on. If you call this column `url` it will make the next step easier. This is also the only column required in the data.

```
$ npm run scrape
```

This will show the help text for the scrape action. You can start scraping with:

```
$ npm run scrape data.csv
```

If you haven't specified a URL column it will ask for it. The script will then go through
retrieving these URLs and getting the appropriate data. It will save the data in `src/_data/projects.json` when it finishes.

Follow the output to see if there are any errors, it will do its best not to crash.

Once that's done you can use

```
$ npm run dev
```

to see the gallery.

## Customising the website

The website is built using [Eleventy](https://www.11ty.dev/), [Tailwind](https://tailwindcss.com/) and [TypeScript](https://www.typescriptlang.org/). Eleventy generates the website, Tailwind is used for styling it and Typescript is for the extra search and random functionality.

You can change the colours by editing the classes like `blue` to be, for example `green`. You can also add your own HTML or change the header. Follow the instructions on the Eleventy and Tailwind websites for more features.

## Hosting the website

You can run build to get a static version of the website:

```
$ npm run build
```

The static version is saved in the `dist` folder.

An easy option for hosting is [Google Firebase](https://firebase.google.com/). It will cost a little bit of money, but I find it's usually at most a few cents per month. Once you've set up an account download the [firebase CLI](https://firebase.google.com/docs/hosting/quickstart) and follow the instructions.

```
$ firebase init .
```

(`.` means the current directory)

Once you've finished setting that up you can deploy it with:

```
$ firebase deploy
```

That should give you a URL for your gallery!

If you want to update it just follow those two steps again:

```
$ npm run build
$ firebase deploy
```

If you've updated your `data.csv` you'll also need to run the scrape script first:

```
$ npm run scrape data.csv
```

Good luck!
