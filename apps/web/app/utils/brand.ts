// One place for the product's identity. The logo files already contain the tagline and "By Tekfolio"
// (primary lockup), so the app does not repeat them as text. Swap the files in public/brand to rebrand.
export const brand = {
  productName: 'EnterpriseSend',
  logo: {
    oneLine: '/brand/logo-one-line.svg',        // header (below 48px high), email and invoice banners
    oneLineDark: '/brand/logo-one-line-dark.svg',
    primary: '/brand/logo-primary.svg',         // sign-in page: two-line lockup with By Tekfolio and tagline
    primaryDark: '/brand/logo-primary-dark.svg',
    loader: '/brand/mark-loader.svg',           // animated four-node mark
    loaderDark: '/brand/mark-loader-dark.svg'
  }
}
