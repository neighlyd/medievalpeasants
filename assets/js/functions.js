function formatCaseDate(data, type, row, meta) {
    if (data) {
        var caseData = meta.settings.json.cases.find(x => x.id === data);
        var sessionData = meta.settings.json.sessions.find(x => x.id === caseData.session);
        var villageData = meta.settings.json.villages.find(x => x.id === sessionData.village);
        return "<a href='" + Urls['case:detail'](data) + "'>" + villageData.name + " | " + sessionData.law_term + ", " + sessionData.year + "</a>";
    } else {
        return "N/A";
    }
}

function formatCase(data, type, row, meta) {
    if (data){
        return "<a href='" + Urls['case:detail'](data.id) + "'>" + data.id + "</a>";
    }
}

function formatPerson(data, type, row, meta) {
    if (data){
        return "<a href='" + Urls['person:detail'](data.id) + "'>" + data.full_name + "</a>";
    }
}

function formatCaseDateNoVillage(data, type, row, meta) {
    if (data.id) {
        return "<a href='" + Urls['case:detail'](data.id) + "'>" + data.law_term + ", " + data.year + "</a>";
    } else {
        return "N/A";
    }
}

function formatSessionDate(data, type, row, meta) {
    if (data.id) {
        return "<a href='" + Urls['session:detail'](data.id) + "'>" + data.village.name + " | " + data.law_term + ", " + data.year + "</a>";
    } else {
        return "N/A";
    }
}

function formatSessionDateNoVillage(data, type, row, meta) {
    if (data) {
        var sessionData = meta.settings.json.sessions.find(x => x.id === data);
        return "<a href='" + Urls['session:detail'](sessionData.id) + "'>" + sessionData.law_term + ", " + sessionData.year + "</a>";
    } else {
        return "N/A";
    }
}

function checkMaker(data) {
    if (data){
        return "<i class='fas fa-check' style='color:forestgreen'></i>";
    } else {
        return "";
    }
}

function checkMakerSubTable(data) {
    if (data){
        return "<i class='fas fa-check' style='color:forestgreen'></i>";
    } else {
        return "";
    }
}

function checkNotes(cellData) {
    if (cellData === "") {
        return '<i class="fas fa-plus-square" aria-hidden="true" style="color: gray" id="check"></i>';
    } else {
        return '<i class="fas fa-plus-square" aria-hidden="true" id="check"></i>';
    }
}

function list_litigants(data){
    var concat = '';
    data.forEach(function (obj, index) {
        concat = concat + '<div class="d-flex justify-content-end">' +
                                '<div class="mr-auto p-0">' +
                                    '<u>Name:</u> ' + '<a href="' + Urls['person:detail'](obj.id) + '">' + obj.name + '</a>' +
                                '</div> ' +
                                '<div class="p-0">' +
                                    '<u>Role:</u> ' + obj.role +
                                '</div>' +
                            '</div>' +
                            '<hr>';
        return concat;
        });
    return concat;

}

function list_parcels(data, type, row, col){
    var concat = '';
    data.forEach(function (obj, index) {
        concat = concat + obj.amount + ' ' + obj.type + ' held by ' + obj.tenure +
                            '<hr>';
        return concat;
        });
    return concat;

}

function formatMoney (data, type, row, col) {
    if (data) {
        if (data.in_denarius){
            return data.amount + "(" + data.in_denarius + "d.)";
        } else {
            return data.amount;
        }
    }
}

function format_person_subdata(data){
    var earliestCase = '';
    if (data.person.earliest_case.id){
        earliestCase = "<a href='" + Urls['case:detail'](data.person.earliest_case.id) +"'>" + data.person.earliest_case.session.law_term + ", " + data.person.earliest_case.session.year + "</a>"
    } else {
        earliestCase = "N/A"
    }
    var latestCase = '';
    if (data.person.latest_case.id){
        latestCase = "<a href='" + Urls['case:detail'](data.person.latest_case.id) +"'>" + data.person.latest_case.session.law_term + ", " + data.person.latest_case.session.year + "</a>"
    } else {
        latestCase = "N/A"
    }
return "<table class='table'>" +
"<tr>" +
"<td><b>Village:</b></td>" +
"<td>" + data.person.village.name + "</td>" +
"<td><b>Gender:</b></td>" +
"<td>" + data.person.gender_display + "</td>" +
"<td><b>Status:</b></td>" +
"<td>" + data.person.status_display + "</td>" +
"</tr>" +
"<tr>" +
"<td><b>Litigation Count:</b></td>" +
"<td>" + data.person.counts.litigation + "</td>" +
"<td><b>Total Case Count:</b></td>" +
"<td>" + data.person.counts.all_cases + "</td>" +
"<td><b>Earliest Case:</b></td>" +
"<td>" + earliestCase + "</td>" +
"<td><b>Latest Case:</b></td>" +
"<td>" + latestCase + "</td>" +
"</tr>" +
"<tr>" +
"<td><b>Amercement Count:</b></td>" +
"<td>" +data.person.counts.monetary.amercement_count + "</td>" +
"<td><b>Fine Count:</b></td>" +
"<td>" + data.person.counts.monetary.fine_count + "</td>" +
"<td><b>Damages Count:</b></td>" +
"<td>" + data.person.counts.monetary.damage_count + "</td>" +
"</tr>" +
"<tr>" +
"<td><b>Chevage Count:</b></td>" +
"<td>" + data.person.counts.monetary.chevage_count + "</td>" +
"<td><b>Impercamenta Count:</b></td>" +
"<td>" + data.person.counts.monetary.impercamentum_count + "</td>" +
"<td><b>Heriot Count:</b></td>" +
"<td>" + data.person.counts.monetary.heriot_count + "</td>" +
"</tr>" +
"</table>"
}