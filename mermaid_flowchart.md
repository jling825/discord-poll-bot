```mermaid
graph TD;
    subgraph Bot Configuration
    Start([Start]) --> process1(Message sent);
    process1 --> data1[/Read message author/];
    data1 --> decision1{Author is client};
    decision1 -- yes --> process2(Ignore message);
    process2 --> End([End]);
    decision1 -- no --> data2[/Read message content/];
    data2 --> decision2{Content is `!whitelist`}
    decision2 -- yes --> process3(Add channel to messages.whitelist)
    process3 --> End
    decision2 -- no --> data3[/Read message channel/]
    data3 --> decision3{Channel is on messages.whitelist}
    decision3 -- no --> process2
    decision3 -- yes --> decision4{Content is `!blacklist`}
    decision4 -- yes --> process4(Remove channel from messages.whitelist)
    process4 --> End
    decision4 -- no --> decision5{Content is `!status`}
    decision5 -- yes --> process5(Print Poll Bot status)
    process5 --> End
    decision5 -- no --> decision6{Content in messages.commands}
    decision6 -- no --> process6(Print messages.help)
    process6 --> End
    end

    subgraph Poll Setup
    decision6 -- yes --> process7(Poll Setup command sent)
    process7 --> decision7{Content is `!newpoll`}
    decision7 -- yes --> process8(Create new poll)
    process8 --> End
    end
    ```