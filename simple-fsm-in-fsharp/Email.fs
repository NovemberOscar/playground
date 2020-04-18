namespace SimpleFsmInFsharp

open System

module Email = 
    type UnverifiedState = { UnverifiedEmail: string; }
    type VerifiedState = { VerifiedEmail: string; VerifiedTime: DateTime}

    type EmailAddress =
        | Unverified of UnverifiedState
        | Verified of VerifiedState

    let verifyForUnverifiedState state time=
        EmailAddress.Verified { VerifiedEmail=state.UnverifiedEmail; VerifiedTime=time}
        
    type UnverifiedState with
        member this.Verify = verifyForUnverifiedState this
        
    let verifyEmailAddress email time =
        match email with
            | Unverified state -> state.Verify time
            | Verified _ ->
                printfn "Error: This email has been verified already."
                email
                
    let displayEmailAddress email =
        match email with
            | Unverified state ->
                printfn "Unverified %s" state.UnverifiedEmail
            | Verified state ->
                printfn "Verified %s (Verified at %A)" state.VerifiedEmail state.VerifiedTime


    type EmailAddress with
        static member New email = EmailAddress.Unverified { UnverifiedEmail=email }
        member this.Verify = verifyEmailAddress this
        member this.Display = displayEmailAddress this

