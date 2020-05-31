async function get_user_data(){
    
    let request = await fetch('/api/user');
    if (!request.ok) {
        throw new Error("Couldn't get user data");
    } else {
        let user_data = await request.json();
        
        update_name(user_data.name);
        update_username(user_data.screen_name);
        update_picture(user_data.profile_image_url);
        update_header(user_data.profile_banner_url);
    }
    
}

// Gets classifiers from backend and saves the information on sessionStorage and requests tweets from get_tweets()
async function prepare_front(){
    try {
        let request = await fetch('/api/classifier');
        if (!request.ok) {
            throw Error("Classifiers couldn't be loaded");
        } else {
            let classifiers = await request.json();
            
            classifiers.forEach(classifier => {
                sessionStorage.setItem(classifier.name, 0);
                get_tweets(classifier.name).then(() => {
                    let language_container = document.querySelector(`#pills-${classifier.name}`);
                    language_container.removeChild(document.querySelector(`#${classifier.name}-load`));
                });
                
            });
            
            
        }
    } catch (error) {
        alert(Error);
    }
}

async function get_tweets(language){
    let currentPage = sessionStorage.getItem(language);
    try{
        let request = await fetch(`/api/tweets/${language}/${currentPage}`);
        if (!request.ok || request.status === 429) {
            throw Error("Tweets couldn't be loaded");
        } else {
            console.log(request);
            let tweets = await request.json();
            
            let language_container = document.querySelector(`#pills-${language}`);
            
            // TODO: Make foreach async so that endtext gets inserted properly
            tweets.forEach(tweet => {
                tweet_container = createTweet(tweet.tweet_id);
                tweet_container.appendChild(createClassifierTrainer(tweet.tweet_id));
                language_container.appendChild(tweet_container);
            });
            
            language_container.appendChild(createEndText());
        }
    } catch (error) {
        let language_container = document.querySelector(`#pills-${language}`);
        if(document.querySelector(`#bottom`)){
            language_container.removeChild(document.querySelector(`#bottom`));
        }
        language_container.appendChild(createErrorEndText());
    }
}

// Creates a container for the tweet and creates a tweet widget inside of it using Twitter Widgets
function createTweet(tweet_id){
    let container = document.createElement('div');
    container.setAttribute('data-tweetid', tweet_id);
    container.classList.add("h-justify-center-content", "h-align-center-content", "h-flex-row-reverse", "h-display-none");
    
    twttr.widgets.createTweet(tweet_id, container, {conversation: 'none'});

    return container;
}

// Creates the like and dislike buttons for each tweet, as well as it's container
function createClassifierTrainer(tweet_id){
    let classifer_train = document.createElement('div');
    classifer_train.classList.add('m-classifier-train');
    classifer_train.id = tweet_id;
    
    let train_text = document.createElement('span');
    train_text.innerHTML = 'Do you like this tweet?';
    train_text.classList.add('m-classifier-train__text');
    
    let like_button = document.createElement('button');
    like_button.classList.add("m-button", "m-button--tweet", "m-button--green", "h-justify-center-content", "h-align-center-content");
    like_button.id = 'like';
    createTrainingEventListener(like_button, tweet_id, 'pos');
    
    let like_icon = document.createElement('i');
    like_icon.classList.add('fas', 'fa-heart', 'm--white');
    
    let dislike_button = document.createElement('button');
    dislike_button.classList.add("m-button", "m-button--tweet", "m-button--red", "m-button--tweet-dislike", "h-justify-center-content", "h-align-center-content");
    dislike_button.id = 'dislike';
    createTrainingEventListener(dislike_button, tweet_id, 'neg');
    
    let dislike_icon = document.createElement('i');
    dislike_icon.classList.add('fas', 'fa-heart-broken', 'm--white');
    
    like_button.appendChild(like_icon);
    dislike_button.appendChild(dislike_icon);
    
    classifer_train.appendChild(train_text);
    classifer_train.appendChild(like_button);
    classifer_train.appendChild(dislike_button);
    
    return classifer_train;
}

function createTrainingEventListener(button, tweet_id, pos_neg){
    button.addEventListener('click', async () => {
        // Show loading icon after request is made
        let loading_container = document.createElement('div');
        loading_container.classList.add('m-loading-button');
        
        let old_button = button.querySelector('svg');
        button.replaceChild(loading_container, old_button);
        try{
            let request = await fetch(`/api/classifier/train`, 
            {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include',
                body: JSON.stringify({sentiment: pos_neg, tweet_id: tweet_id, language: getCurrentTab()})
                
            });
            
            if (!request.ok) {
                throw Error("Classifier couldn't be trained");
            } else {
                
                // When the classifier was trained succesfully
                await request.json().then(() => {
                    // Change to success icon
                    let success_icon = document.createElement('i');
                    success_icon.classList.add('fas', 'fa-check-circle', 'm--white');
                    
                    button.replaceChild(success_icon, loading_container);
                    
                    // Disable buttons
                    // This gets all of the buttons inside the trainer container
                    let trainer = button.parentElement.querySelectorAll('button');
                    trainer.forEach(element => {
                        element.disabled = true;
                    });
                    
                });
                
            }
        } catch (error) {
            // TODO: Icon if promise fails
            alert(error);
        }
    });
}

function createEndText(){
    let text_container = document.createElement('div');
    text_container.id = 'bottom';

    let text = document.createElement('p');
    text.innerHTML = "Looks like you've reached the end... (Loading more tweets...)";

    text_container.appendChild(text);
    
    return text_container;
}

function createErrorEndText(){
    let text_container = document.createElement('div');
    text_container.id = 'bottom-true';

    let text = document.createElement('p');
    text.innerHTML = "Looks like you've reached the <b>true</b> end... <br> Twitter limits the amounts of requests we can make per day. Please try again later.";

    text_container.appendChild(text);
    
    return text_container;
}

function update_name(new_name){
    document.querySelector('#name').innerHTML = new_name;
}

function update_username(new_username){
    document.querySelector('#username').innerHTML = `@${new_username}`;

}

function update_picture(new_picture){
    document.querySelector('#picture').style.backgroundImage = `url(${new_picture})` ;
}

function update_header(new_picture){
    document.querySelector('#header').style.backgroundImage = `url(${new_picture})` ;
}

function getCurrentTab(){
    return document.querySelector('.active').dataset.language;
}

window.onscroll = () => {
    let title = document.querySelector('#header-title');
    
    // Holds current position of the document
    let position = document.querySelector('body').getBoundingClientRect();
    
    // Checks when page is scrolled 100 units down
    if (position.y >= -100) {
        title.classList.remove("h-slide-bottom");
        title.classList.add("h-slide-top");
    } else {
        // When page is scrolled down:
        title.classList.remove("h-slide-top");
        title.classList.add("h-slide-bottom");
        title.classList.remove("h-display-none");
    }
    
    // TODO: Non jQuery implementarion
    // Checks when page is scrolled to the bottom
    if($(window).scrollTop() + $(window).height() == $(document).height()) {
        let language = getCurrentTab();
        let currentPage = Number(sessionStorage.getItem(language));
        currentPage++;
        
        sessionStorage.setItem(language, currentPage);
        
        get_tweets(language).then(() => {
            let language_container = document.querySelector(`#pills-${language}`);
            language_container.removeChild(document.querySelector(`#bottom`));
        });
    }
};

window.onload = () => {
    document.querySelector('.tab-pane').classList.add("active", "show")
    document.querySelector('.nav-link').classList.add("active")
    
    get_user_data();
    prepare_front();

    twttr.events.bind(
        'rendered',
        function (event) {
          event.target.parentNode.classList.remove('h-display-none');
          event.target.parentNode.classList.add('h-slide-bottom');
        }
    );

    document.querySelector('#logout').addEventListener('click', async () =>{
        window.location.replace('/logout');
    });
};