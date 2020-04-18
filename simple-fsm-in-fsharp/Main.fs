// Learn more about F# at http://fsharp.org

open System
open SimpleFsmInFsharp.Email


let unverifiedEmail = EmailAddress.New "user@example.com"
printf "unverifiedEmail = " ; unverifiedEmail.Display

let verifiedEmail = unverifiedEmail.Verify DateTime.Now
printf "verifiedEmail = " ; verifiedEmail.Display

let verifiedAgainEmail = verifiedEmail.Verify DateTime.Now
printf "verifiedAgainEmail = " ; verifiedAgainEmail.Display

[<EntryPoint>]
let main argv = 0
