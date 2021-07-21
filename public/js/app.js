
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
  locker.hook_after_login = load_data
  //document.getElementById('authentication').style.display = 'block'
  s = await locker.check_login()
  check_and_redirect(s)
}

function create_app(){
  appname = document.getElementById("new_app_name").value
  console.log('create app', appname)
  locker.post('~/rw/create.json', {
    action: 'append',
    default: [],
    e: appname
  }).then( r => {
    locker.set_flag('updated')
    .then(r => {
      console.log("sent request to create application")
    })
  })
}

async function load_data(){
  draw_profile()
}

async function draw_profile(){
  locker.get_json_file('~/r/userinfo.json', data => {
    document.getElementById("profile").innerText = `Hello, ${data['name']} <${data['email']}>!`
  })
}

async function logout(){
  locker.logout()
  window.location.href = '/login.html'
}

