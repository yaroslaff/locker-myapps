
locker = new Locker(locker_addr)
//locker.hook_after_check_login = app_hook_redirect
locker.hook_after_logout = check_and_redirect
locker.return_url = new URL('/dashboard.html', window.location.href).href

function check_and_redirect(s){

  if(!s.status && window.location.pathname!='/login.html'){
    window.location.href = '/login.html'
    return
  }

  if(s.status && (window.location.pathname=='/' || window.location.pathname=='/index.html')){
    window.location.href = '/dashboard.html'
    return
  }
}


window.onload = async () => {
  //locker.hook_after_login = load_data
  //document.getElementById('authentication').style.display = 'block'
  s = await locker.check_login()
  check_and_redirect(s)
  
  // here we're logged in
  load_data()
}

function create_app(){
  appname = document.getElementById("new_app_name").value
  console.log('create app', appname)
  locker.post('~/rw/requests.json', {
    action: 'append',
    default: [],
    e: {
      'name': appname,
      'command': 'create_app',
      '_timestamp': null
    }
  }).then( r => {
    locker.set_flag('updated')
    .then(r => {
      console.log("sent request to create application")
      
      // update table
      draw_create_requests()
    })
  })
}

async function load_data(){
  draw_profile()
  draw_create_requests()
  draw_apps()
}

function draw_profile(){
  locker.get_json_file('~/r/userinfo.json', p => {console.log("profile: %o", p)})
}


function render_create_request(app){

  const status = 'Pending'
  const details = 'Waiting to be created'

  console.log(app.name)


  return `
      <tr class="text-gray-700 dark:text-gray-400">
      <td class="px-4 py-3">
        <div class="flex items-center text-sm">
          <div>
            <p class="font-semibold">${app.name}</p>
            <p class="text-xs text-gray-600 dark:text-gray-400">
              ${app.subtitle}
            </p>
          </div>
        </div>
      </td>
      <td class="px-4 py-3 text-xs">
        <span
          class="px-2 py-1 font-semibold leading-tight text-green-700 bg-green-100 rounded-full dark:bg-green-700 dark:text-green-100"
        >
          ${status}
        </span>
      </td>
      <td class="px-4 py-3 text-sm">
        ${details}
      </td>
      <td class="px-4 py-3">
        <div class="flex items-center space-x-4 text-sm">
          <button
            class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
            aria-label="Delete"
          >
            <svg
              class="w-5 h-5"
              aria-hidden="true"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
        </div>
      </td>
    </tr>
  `
}

function render_app(app){
  console.log(app.name)

  const status = 'Pending'
  const details = 'Waiting to be created'

  return `
      <tr class="text-gray-700 dark:text-gray-400">
      <td class="px-4 py-3">
        <div class="flex items-center text-sm">
          <div>
            <p class="font-semibold">${app.name}</p>
            <p class="text-xs text-gray-600 dark:text-gray-400">
              ${app.subtitle}
            </p>
          </div>
        </div>
      </td>
      <td class="px-4 py-3 text-xs">
        <span
          class="px-2 py-1 font-semibold leading-tight text-green-700 bg-green-100 rounded-full dark:bg-green-700 dark:text-green-100"
        >
          ${app.status}
        </span>
      </td>
      <td class="px-4 py-3 text-sm">
        ${app.details}
      </td>
      <td class="px-4 py-3">
        <div class="flex items-center space-x-4 text-sm">
          <button
            class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
            aria-label="Edit"
          >
            <svg
              class="w-5 h-5"
              aria-hidden="true"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
              ></path>
            </svg>
          </button>
          <button
            class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray"
            aria-label="Delete"
          >
            <svg
              class="w-5 h-5"
              aria-hidden="true"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
        </div>
      </td>
    </tr>
  `
}





function draw_create_requests(){

  const e = document.getElementById('requests-tbody')

  locker.get('~/rw/requests.json')
    .then( r => { 
      if (!r.ok) {
        // make the promise be rejected if we didn't get a 2xx response
        throw new Error("Not 2xx response")
      }
      return r.json() } )
    .then( r => {
      console.log("create: %o", r)
      e.innerHTML = ''

      r.forEach(req => {
        const app = {
          'name': req.name, 
        }
        console.log("draw request: %o", app)
        e.innerHTML += render_create_request(app)
      });
    })
    .catch( e => {
      console.log("ERR: %o", e)
    })
}


function draw_apps(){

  const e = document.getElementById('apps-tbody')

  locker.get('~/r/apps.json')
  .then( r => { 
    if (!r.ok) {
      // make the promise be rejected if we didn't get a 2xx response
      throw new Error("Not 2xx response")
    }
    return r.json() } )
  .then( r => {
    //console.log("create: %o", r)
    e.innerHTML = ''

    for(let name in r){
      app = r[name]
      // console.log("draw: %o %o", app, e)
      e.innerHTML += render_app(app)
    }
  })
  .catch( e => {
    console.log("ERR: %o", e)
  })
}

async function logout(){
  locker.logout()
  window.location.href = '/login.html'
}

