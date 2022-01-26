const auth_get_data = (url) =>{

        return fetch(url, {
            method: 'GET',
            headers: {
                'Content-type': 'application/json;charset=UTF-8',
                'Authorization': 'Token '+ localStorage.getItem('token')},
        })
            .then(res => {
                return res.json()
            })
            .then(data => {

                if (data.detail === 'Invalid authentication. Could not decode token.'){
                    window.location.replace('/sign-in/');
                }
                return data;
            })

            .catch((error) => {
                console.log(error)
            })
    }


export default auth_get_data
