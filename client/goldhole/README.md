# goldhole client

## Project setup

```
npm install
npm install --global serve OR npx serve (package.json assumes you have serve)
```

Create a `.env.development.local` file with the `VUE_APP_API_URL` variable in it. Should point to your local instance of the API.

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Builds and serves production

```
npm run start
```

### Lints and fixes files

```
npm run lint
```

## Code tour

- File structure largely follows what's practiced in [Vue docs](https://vuejs.org/guide/introduction.html#still-got-questions) but here's a QRD if you're new or I'm wrong
  - `service` - stores API calls. `ApiFactory` pattern used for each call (eg: `new ApiFactory("users")`)
  - `store` state. doesn't use vuex
  - rest should be standard (eg: `views` = pages)
