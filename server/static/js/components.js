export const numpad = `
<div class="screen animate__animated animate__fadeInDown animate__fast">
    <div class="keyboard">
        <div class="display">
            <div class="col-span-2 text-center text-xl">
                > 
            </div>
            <div class="col-span-4 text-center text-xl">
                __  __  __  __
            </div>
        </div>
        <button>
            <span>7</span>
        </button>
        <button>
            <span>8</span>
        </button>
        <button>
            <span>9</span>
        </button>
        <button>
            <span>4</span>
        </button>
        <button>
            <span>5</span>
        </button>
        <button>
            <span>6</span>
        </button>
        <button>
            <span>1</span>
        </button>
        <button>
            <span>2</span>
        </button>
        <button>
            <span>3</span>
        </button>
        <button>
        <span class="text-xl">Delete</span>
        </button>
        <button>
            <span>0</span>
        </button>
        <button>
        <span class="text-xl">Done</span>
        </button>
    </div>
</div>
`

export const alertErr = `
<div class="bg-red-100 border border-red-400 text-red-700 text-center px-4 py-3 mb-4 rounded w-auto inline-block mx-auto animate__animated animate__fadeIn" role="alert">
  <strong class="font-bold">User not indentified</strong>
  <span class="block sm:inline"> Please insert a pin code to enter into the system</span>
</div>
`

export const retryLogin = `
<a href="/login" class="animate__animated animate__fadeIn m-3 w-min ml-auto bg-highlight hover:bg-blue-400 text-main fill-main font-bold py-2 px-4 border-b-4 border-headline hover:border-blue-500 rounded-md">
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2v6h-6"></path><path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path><path d="M3 22v-6h6"></path><path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path></svg>
</a>
`