
locker = new Locker(locker_addr)

window.onload = async () => {
  locker.hook_login = load_data
  document.getElementById('authentication').style.display = 'block'
  locker.check_login()  
}


function create_app(){
  appname = document.getElementById("appname").value
  console.log('create app', appname)
  locker.post('~/rw/create.json', {
    action: 'append',
    default: [],
    e: appname
  }).then( r => {
    locker.set_flag('updated')
    .then(r => {
      console.log("set_flag", r)
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
}
