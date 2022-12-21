from preprocessing import processing_pipeline

test_song = {
    "Song": "Mockingbird",
    "Artist": "Eminem",
    "Lyrics": (
        """Yeah
        I know sometimes things may not always make sense to you right now
        But hey, what daddy always tell you?
        Straighten up little soldier
        Stiffen up that upper lip
        What you crying about?
        You got me
        Hailie, I know you miss your mom, and I know you miss your dad
        When I'm gone, but I'm trying to give you the life that I never had
        I can see you're sad, even when you smile, even when you laugh
        I can see it in your eyes, deep inside you want to cry
        'Cause you're scared, I ain't there, daddy's with you in your prayers
        No more crying, wipe them tears, daddy's here, no more nightmares
        We gon' pull together through it, we gon' do it
        Laney uncle's crazy, ain't he? Yeah, but he loves you girl and you better know it
        We're all we got in this world, when it spins, when it swirls
        When it whirls, when it twirls, two little beautiful girls
        Lookin' puzzled, in a daze, I know it's confusing you
        Daddy's always on the move, mamma's always on the news
        I try to keep you sheltered from it, but somehow it seems
        The harder that I try to do that, the more it backfires on me
        All the things growing up, his daddy, daddy had to see
        Daddy don't want you to see, but you see just as much as he did
        We did not plan it to be this way, your mother and me
        But things have gotten so bad between us, I don't see us ever being together
        Ever again like we used to be when we was teenagers
        But then of course everything always happens for a reason
        I guess it was never meant to be
        But it's just something we have no control, over and that's what destiny is
        But no more worries, rest your head and go to sleep
        Maybe one day we'll wake up, and this will all just be a dream
        Now hush little baby, don't you cry
        Everything's gonna be alright
        Stiffen that upper-lip up, little lady, I told ya
        Daddy's here to hold ya through the night
        I know mommy's not here right now, and we don't know why
        We fear how we feel inside
        It may seem a little crazy, pretty baby
        But I promise momma's gon' be alright
        Huh, it's funny
        I remember back one year when daddy had no money
        Mommy wrapped the Christmas presents up and stuck 'em under the tree
        And said, "Some of 'em were from me, 'cause Daddy couldn't buy 'em"
        I'll never forget that Christmas, I sat up the whole night crying
        'Cause daddy felt like a bum
        See daddy had a job
        But his job was to keep the food on the table for you and mom
        And at the time every house that we lived in
        Either kept getting broke into and robbed
        Or shot up on the block
        And your Mom was saving money for you in a jar
        Tryna start a piggy bank for you, so you could go to college
        Almost had a thousand dollars 'til someone broke in and stole it
        And I know it hurt so bad, it broke your momma's heart
        And it seemed like everything was just startin' to fall apart
        Mom and dad was arguin' a lot, so momma moved back
        On the Chalmers in the flat one-bedroom apartment
        And dad moved back to the other side of 8 Mile on Novara
        And that's when daddy went to California with his C.D
        And met Dr. Dre, and flew you and momma out to see me
        But daddy had to work, you and momma had to leave me
        Then you started seeing daddy on the T.V
        And momma didn't like it, and you and Laney were to young to understand it
        Papa was a rollin' stone, momma developed a habit
        And it all happened too fast for either one of us to grab it
        I'm just sorry you were there and had to witness it first hand
        'Cause all I ever wanted to do was just make you proud
        Now I'm sittin' in this empty house
        Just reminiscing, lookin' at your baby pictures
        It just trips me out
        To see how much you both have grown
        It's almost like you're sisters now
        Wow, guess you pretty much are, and daddy's still here
        Laney, I'm talkin' to you too, daddy's still here
        I like the sound of that, yeah, It's got a ring to it, don't it?
        Shh, momma's only gone for the moment
        Now hush little baby, don't you cry
        Everything's gonna be alright
        Stiffen that upper-lip up, little lady, I told ya
        Daddy's here to hold ya through the night
        I know mommy's not here right now, and we don't know why
        We fear how we feel inside
        It may seem a little crazy, pretty baby
        But I promise, momma's gon' be alright
        And if you ask me too
        Daddy's gonna buy you a Mockingbird
        I'ma give you the world
        I'ma buy a diamond ring for you, I'ma sing for you
        I'll do anything for you to see you smile
        And if that Mockingbird don't sing, and that ring don't shine
        I'ma break that birdies neck
        I'd go back to the jeweler who sold it to ya
        And make him eat every karat, don't fuck with dad (haha)"""
    ),
}

processing_pipeline(test_song)
