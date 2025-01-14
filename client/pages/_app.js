import '@/styles/globals.css'
import { ThemeProvider } from 'next-themes'
import Navbar from '@/components/Navbar'
import { SessionProvider } from 'next-auth/react'
import { TokenProvider } from '@/context/tokenContext'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

export default function App({
    Component,
    pageProps: { session, ...pageProps },
}) {
    return (
        <div className={'p-4 max-w-[1216px] w-full m-auto'}>
            <ThemeProvider attribute="class" defaultTheme="system">
                <SessionProvider session={session}>
                    <TokenProvider>
                        <Navbar />
                        <Component {...pageProps} />
                    </TokenProvider>
                    <ToastContainer />
                </SessionProvider>
            </ThemeProvider>
        </div>
    )
}
